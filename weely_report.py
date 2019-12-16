import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import string

filename = 'data.txt'
with open(filename) as fobj:
    lines = fobj.readlines()
    
day_abbrs = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
jobs_in_week = [{} for day in range(7)]

for line in lines:
    if len(line) > len('\n'):
        if line.strip().upper() in day_abbrs:
            day = day_abbrs.index(line.strip().upper())
            
        else:
            job_name = ''
            job_time = 0
            items = line.split()
            if len(items) >= 2:
                for item in items:
                    if item.startswith(tuple(string.ascii_letters)) or\
                        item.startswith('&'):
                        job_name += item
                        job_name += ' '
                    elif item.endswith(('h', 'H')):
                        job_time += 60 * int(item[0:-1])
                    else:
                        job_time += int(item)
            job_name = job_name.strip()
            jobs_in_week[day][job_name] = job_time
            
def get_ave_sleep_time(jobs_in_week):
    slcnt = 0
    slsum = 0
    for day in range(7):
        if 'sl' in jobs_in_week[day]:
            slcnt += 1
            slsum += jobs_in_week[day]['sl']
    return slsum/slcnt
sl_avg = get_ave_sleep_time(jobs_in_week)

sleep_times = []
for day in range(7):
    if 'sl' not in jobs_in_week[day]:
        sleep_times.append(sl_avg)
    else:
        sleep_times.append(jobs_in_week[day]['sl'])

work_times = []
for day in range(7):
    working_time = 0
    for job_name in jobs_in_week[day]:
        if job_name != 'sl':
            working_time += jobs_in_week[day][job_name]
    work_times.append(working_time)    

# Draw vertical report
x = np.arange(len(day_abbrs))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, sleep_times, width, label='Sleep')
rects2 = ax.bar(x + width/2, work_times, width, label='Work')

ax.set_ylabel('Time in minutes')
ax.set_title('Weekly Time Report')
ax.set_xticks(x)
ax.set_xticklabels(day_abbrs)
plt.yticks(np.arange(0, max(work_times)+100, 100))

ax.legend()

def get_time_string(minute):
    minute = int(minute)
    if minute >= 60:
        return str(minute//60) + 'h' + (str(minute%60) if minute%60 else '')
    else:
        return str(minute)
    
def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate(
#                     '{}'.format(int(height)),
                    get_time_string(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom'
        )

autolabel(rects1)
autolabel(rects2)

# Shrink current axis by 20%
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.show()
plt.savefig('data1.png')


jobs_sum = {}
for jobs in jobs_in_week:
    for job in jobs:
        if job not in jobs_sum:
            jobs_sum[job] = jobs[job]
        else:
            jobs_sum[job] += jobs[job]
for job in jobs_sum:
    jobs_sum[job] = jobs_sum[job] / 60
jobs_sum = {k: v for k, v in sorted(jobs_sum.items(), key=lambda item: item[1], reverse=True)}

plt.rcdefaults()
fig, ax = plt.subplots()
jobs = jobs_sum.keys()
y_pos = np.arange(len(jobs))
time = jobs_sum.values()

ax.barh(y_pos, time,  align='center')
ax.set_yticks(y_pos)
ax.set_yticklabels(jobs)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Hours')
plt.xticks(np.arange(0, max(time)+5, 5))
ax.set_title('Time Spend In Each Activity')

for i, v in enumerate(time):
    ax.text(v + .3, i + .25, '{:.1f}'.format(v))
    
total = sum(jobs_sum.values()) - jobs_sum['sl']
ax.text(0.95, 0.01, 
        'excluding sleep:  {:.1f} / {:.1f}'.format(total, total/7),
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax.transAxes,
        fontsize=13
       )

total +=  sl_avg * 7 / 60
ax.text(0.95, 0.10, 
        'including sleep: {:.1f} / {:.1f}'.format(total, total/7),
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax.transAxes,
        fontsize=13
       )
    
plt.savefig('data2.png')
# plt.show()