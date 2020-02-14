from datetime import date, timedelta
import datetime

# 2019.9.2 - 2020.1.12
begin = date(2019, 9, 2)
end = date(2020, 1, 13)
one_day = timedelta(days=1)
day_abbrs = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']

output = ''
week_cnt = 0
cur = begin
while cur < end:
    # make title: '--Week n--'
    if cur.isoweekday() == 1:
        week_cnt += 1
        title = 'Week {}'.format(week_cnt)
        title = title.rjust(23, '-')
        title = title.ljust(40, '-')
        output += title + '\n'

    # weekday, date: '* MON, 2019-11-9'
    output += '*' + day_abbrs[cur.weekday()] + ', ' + str(cur) + '\n\n'

    # next day
    cur = cur + one_day

file_name = str(begin) + '-' + str(end) + '.txt'
with open(file_name, 'w') as f:
    f.write(output)
