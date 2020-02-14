import os

'''
Parse the records into format: activity duration_in_minutes,
parse (abbreviation, full_name) pair for ecah activity at the same time.
The result is stored in lines and abbrs individually.
'''

from db_mngr import DBMngr


class RecordParser:
    def __init__(self, file_name):
        self.file_name = file_name
        self.lines = []
        self.abbrs = {}

    def parse(self):
        self.read_file()
        self.remove_empty_lines()

        self.parse_abbreviation_of_activities()
        self.parse_to_activity_duration()
        self.parse_to_date_activity_duration()

        self.check_unique_key()
        self.insert_to_database()
        self.check_typo()

    def read_file(self):
        with open(self.file_name, 'r') as f:
            self.lines = f.readlines()

    def remove_empty_lines(self):
        for line in self.lines:
            if len(line) <= 1:
                self.lines.remove(line)

        # remove trailing '\n'
        for idx in range(len(self.lines)):
            if self.lines[idx].endswith('\n'):
                self.lines[idx] = self.lines[idx][:-1]

    def parse_abbreviation_of_activities(self):
        for line in self.lines:
            if line.find('=') != -1:
                self.parse_abbreviation(line)

    def parse_abbreviation(self, line):
        ''' dp = design pattern 1h30 '''
        # abbr = 'dp'
        abbr = line[0:line.index('=')].strip().lower()

        # line_without_abbr = ' design pattern 1h30'
        line_without_abbr = line[line.index('=')+1:]

        index_of_first_digit = 0
        for char in line_without_abbr:
            if char.isdigit():
                index_of_first_digit = line_without_abbr.find(char)
                break

        # full_name = 'design pattern'
        full_name = line_without_abbr[:index_of_first_digit].strip().lower()

        # check full_name legality
        if len(full_name) == 0:
            print('Wraning: full_name is NULL in record "{}"'.format(line))

        # check name collision
        if abbr in self.abbrs and self.abbrs[abbr] != full_name:
            print('Wraning: {} = {} overwritten by {}'.format(
                abbr, self.abbrs[abbr], full_name
            ))

        self.abbrs[abbr] = full_name

    def parse_to_activity_duration(self):
        ''' convert lines to format 'activety, time_in_minutes' '''
        for idx in range(len(self.lines)):
            if self.lines[idx].startswith(('-', '*')):
                continue
            else:
                # get start position of duration
                idx_of_first_digit = 0
                for char in self.lines[idx]:
                    if char.isdigit():
                        idx_of_first_digit = self.lines[idx].find(char)
                        break

                # get full name
                if '=' in self.lines[idx]:
                    idx_of_equal_sign = self.lines[idx].index('=')
                    full_name = self.lines[idx][idx_of_equal_sign+1: idx_of_first_digit]\
                        .strip().lower()
                else:
                    activity = self.lines[idx][:idx_of_first_digit]\
                        .strip().lower()
                    if '_' in activity:
                        # db_exp
                        prefix, suffix = activity.split('_')
                        prefix.strip()
                        suffix.strip()

                        if prefix in self.abbrs:
                            full_name = self.abbrs[prefix] + ' ' + suffix
                        else:
                            full_name = prefix + ' ' + suffix
                    else:
                        if activity in self.abbrs:
                            full_name = self.abbrs[activity]
                        else:
                            full_name = activity

                # convert duration to minutes
                duration = self.lines[idx][idx_of_first_digit:].strip().lower()
                minute = 0
                if 'h' in duration:
                    # 1h
                    if duration.endswith('h'):
                        minute = int(
                            float(duration[:duration.index('h')]) * 60)
                    # 1h30
                    else:
                        hour, minute = duration.split(sep='h')
                        minute = 60*int(hour) + int(minute)
                else:
                    # 90
                    try:
                        minute = int(duration)
                    except ValueError as e:
                        print(e)

                    if minute <= 5:
                        print('Warning: only {} minutes, "{}"'.format(
                            minute, self.lines[idx])
                        )

                # replase line with parsing result
                self.lines[idx] = full_name + ',' + str(minute)

    def parse_to_date_activity_duration(self):
        ''' convert lines to format 'date, activety, time_in_minutes' '''
        for idx in range(len(self.lines)):
            if self.lines[idx].startswith(('-')):
                continue
            elif self.lines[idx].startswith(('*')):
                # 'MON, 2020-01-10' --> '2020-01-10' --> '20200110'
                date = self.lines[idx].split(',')[1].strip()
                date = int(date.replace('-', ''))
            else:
                self.lines[idx] = str(date) + ',' + self.lines[idx]

    def check_unique_key(self):
        '''Check primary key (date, activity) is unique'''
        keys = {}
        for line in self.lines:
            if line.startswith(('-', '*')):
                continue
            else:
                date, activity, duration = line.split(',')
                date = int(date)
                activity = activity.strip()
                duration = duration.strip()

                if (date, activity) not in keys:
                    keys[(date, activity)] = duration
                else:
                    print('Error: {} duplicate'.format((date, activity)))

    def insert_to_database(self):
        records = []
        for line in self.lines:
            if line.startswith(('-', '*')):
                continue
            else:
                date, activity, duration = line.split(',')
                date = int(date)
                activity = activity.strip()
                duration = duration.strip()

                records.append((date, activity, duration))
        
        db = DBMngr()
        db.create_db()
        db.insertmany(records)

    def check_typo(self):
        '''
        Count occurences of each activity.
        If only a small number of records exist in database,
        this activity may be a typo.
        '''

        db = DBMngr()
        query = '''
            Select activity, COUNT(*)
            From Records
            Group By activity
            '''
        for row in db.cur.execute(query):
            if row[1] <= 2:
                print('Warning: "{activity}" maybe a typo, '
                      'cause it only occur {count} times.'
                    .format(activity=row[0], count=row[1]))
        
    def total_worktime(self):
        query = '''
            Select Sum(sum_d)
            From (
                Select SUM(duration) as sum_d
                From Records
                Where 
                    Activity != 'sleep' AND
                    Activity != 'reading'
            )
        '''

        db = DBMngr()

        total_worktime = db.cur.execute(query).fetchone()[0]


if __name__ == '__main__':
    rg = RecordParser('test_data.txt')
    rg.parse()

    # for line in rg.lines:
    #     if len(line) > 1 and not line.startswith(('-', '*')):
    #         # print(line)
    #         pass

    if os.path.exists('records.db'):
        pass
        # os.remove('records.db')
