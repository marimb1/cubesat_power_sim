import sys
sys.path.append('..')
from bat_model import *
from scipy.stats import pearsonr
import csv

# charge_discharge(0.6,0)
# i=1
# while True:
#     charge_discharge(0.6,i)
#     result_t.append(i)
#     i+=1
#     if result_v[-1]<2.65:
#         t=i
#         break
# with open('./simulation_0_6mA.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerow(result_t)
#     writer.writerow(result_v)


time_1_5_exp=[]
voltage_1_5_exp=[]
current_1_5_exp=[]


with open('./discharge_comp_1_5.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    i=0
    for row in reader:
        if i==0:
            r=[float(i) for i in row ]
            time_1_5_exp=r
        if i==1:
            r=[float(i) for i in row ]
            voltage_1_5_exp=r
        i+=1

time_600_exp=[]
volt_600_exp=[]
curr_600_exp=[]

with open('./discharge_comp_600mA.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    i=0
    for row in reader:
        if i==0:
            r=[float(i) for i in row ]
            time_600_exp=r
        if i==1:
            r=[float(i) for i in row ]
            volt_600_exp=r
        i+=1

time_600_sim=[]
volt_600_sim=[]
with open('./simulation_0_6mA.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    i=0
    for row in reader:
        if i==0:
            r=[float(i) for i in row ]
            time_600_sim=r
        if i==1:
            r=[float(i) for i in row ]
            volt_600_sim=r
        i+=1

time_1_5_sim=[]
volt_1_5_sim=[]
with open('./simulation_1_5mA.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    i=0
    for row in reader:
        if i==0:
            r=[float(i) for i in row ]
            time_1_5_sim=r
        if i==1:
            r=[float(i) for i in row ]
            volt_1_5_sim=r
        i+=1

cap_exp_1_5=[i*1.5/60/60 for i in time_1_5_exp]
cap_sim_1_5=[i*1.5/60/60 for i in time_1_5_sim]
cap_exp_0_6=[i*0.6/60/60 for i in time_600_exp]
cap_sim_0_6=[i*0.6/60/60 for i in time_600_sim]

plt.figure(figsize=(10,6))
plt.plot(cap_exp_1_5,voltage_1_5_exp,label='Experiment 1.5A',color='darkorange')
plt.plot(cap_sim_1_5,volt_1_5_sim,label='Simulation 1.5A',color='gold')

plt.plot(cap_exp_0_6,volt_600_exp,label='Experiment 0.6A',color='limegreen')
plt.plot(cap_sim_0_6,volt_600_sim,label='Simulation 0.6A',color='forestgreen')

plt.legend(fontsize=13)
plt.xlabel('Discharge capacity [Ah]',fontsize=15)
plt.xticks(fontsize=13)
plt.yticks(fontsize=13)
plt.ylabel('Voltage [V]',fontsize=15)
plt.savefig('./Plots/discharge_curves_1500mA.pdf')
plt.show()


a=voltage_1_5_exp
b=volt_1_5_sim
for i in range(0,len(voltage_1_5_exp)-len(volt_1_5_sim)):
    b.append(0)

rv=pearsonr(a,b)
print(rv)

# i=0
# t=[]
# volt3=[]
# while i<15000:
#     charge_discharge(-2,i)
#     i+=1
# i=0
# while True:
#     charge_discharge(2,i)
#     i+=1
#     t.append(i)
#     volt3.append(result_v[-1])
#     if result_v[-1]<2.65:
#         break
# print(len(t))
# print(len(volt3))


# plt.plot(time2,volt2,label='Experiment 2A')
# plt.plot(t,volt3,label='Simulation 2A')
# plt.legend()
# plt.xlabel('time [s]')
# plt.ylabel('Volt [V]')
# plt.savefig('./fig/battery_simulation_measurement.pdf')
# plt.show()

