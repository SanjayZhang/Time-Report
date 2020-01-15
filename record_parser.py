'''
Parse the records into format: activity duration_in_minutes,
parse (abbreviation, full_name) pair for ecah activity at the same time.
The result is stored in lines and abbrs individually.
'''
class RecordParser:
    def __init__(self, file_name):
        self.file_name = file_name
        self.lines = []
        self.abbrs = {}
        self.parse()

    def parse(self):
        self.read_file()
        self.remove_empty_lines()
        self.parse_abbreviation_of_activities()
        self.parse_activity_records()

    def read_file(self):
        with open(self.file_name, 'r') as f:
            self.lines = f.readlines()
    
    def remove_empty_lines(self):
        for line in self.lines:
            if len(line) <= 1:
                self.lines.remove(line)
                    
    def parse_abbreviation_of_activities(self):
        for line in self.lines:
            if line.find('=') != -1:
                self.parse_abbreviation(line)

    def parse_abbreviation(self, line):
        ''' dp = design pattern 1h30 '''
        # abbr = 'dp'
        abbr = line[0:line.index('=')].strip().lower()

        # line = ' design pattern 1h30'
        line = line[line.index('=')+1:]

        index_of_first_digit = 0
        for char in line:
            if char.isdigit():
                index_of_first_digit = line.find(char)
                break

        # full_name = 'design pattern'
        full_name = line[:index_of_first_digit].strip().lower() 

        self.abbrs[abbr] = full_name

    def parse_activity_records(self):
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
                    full_name = self.lines[idx]\
                        [idx_of_equal_sign+1 : idx_of_first_digit]\
                        .strip().lower()
                else:
                    full_name = self.lines[idx]\
                        [:idx_of_first_digit]\
                        .strip().lower()

                # convert duration to minutes
                duration = self.lines[idx][idx_of_first_digit:].strip().lower()
                minute = 0
                if 'h' in duration:
                    # 1h
                    if duration.endswith('h'):
                        minute = int(duration[:duration.index('h')]) * 60
                    # 1h30
                    else:
                        hour, minute = duration.split(sep='h')
                        minute = 60*int(hour) + int(minute)
                else:
                    # 90
                    minute = int(duration)

                # replase line with parsing result
                self.lines[idx] = full_name + ' ' + str(minute)



if __name__=='__main__':
    rg = RecordParser('test_data.txt')
    for line in rg.lines[0:38]:
        print(line)

    