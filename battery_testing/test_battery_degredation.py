import sys
sys.path.append('..')
from bat_model import *

import csv


two_years=2*365*24*60*60

i=1
charge_discharge(1,0)
day=0
while True:
    if i>(day*86400):
        day+=1
        print(day)
    while True:
        charge_discharge(1,i)
        result_t.append(i)
        i+=10
        if result_v[-1]<2.65:
            break
    while True:
        charge_discharge(-1,i)
        result_t.append(i)
        i+=10
        if result_v[-1]>4:
            break
    if i > two_years:
        break

cap_percent=[i/cap[0]*100 for i in cap]
seconds_days=[i/86400 for i in result_t]
print(cap_percent[-1])
print(cap[0])
plt.figure(figsize=(10,6))
plt.plot(seconds_days,cap_percent)
plt.title('Battery degredation over time',fontsize=18)
plt.xlabel('Time [d]',fontsize=15)
plt.xticks(fontsize=15)
plt.ylabel('Available capacity [%]',fontsize=15)
plt.yticks(fontsize=15)

plt.savefig('./Plots/battery_degredation_two_years_fullV.pdf')

with open('./Plots/battery_degredation_two_years_fullV.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(result_t)
    writer.writerow(seconds_days)
    writer.writerow(cap)
    writer.writerow(cap_percent)