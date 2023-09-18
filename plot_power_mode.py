import math
import matplotlib.pyplot as plt
from powermodes import *
import numpy as np

power_5=[]
power_3=[]
power_bat=[]
mode=['detumble','deploy','Tx_initial_round','Charge','Split','Pointing','Desaturation','TX_regular','RX_regular','Spin_Up','Spin_Down','Experiment','GNSS_positioning_scientific','GNSS_positioning_pvt','Beacon','Critical','Emergency']
def addlabels(x,y,z):
    for i in range(len(x)):
        if y[i]>=0.5:
            plt.text(i, y[i]+z[i]-0.8, round(y[i],1), ha = 'center')

def addlabels2(x,y):
    for i in range(len(x)):
        if y[i]>=0.5:
            plt.text(i, y[i]-0.8, round(y[i],1), ha = 'center')


for element in mode:
    v5=0
    v3=0
    vbat=0
    v3,v5,vbat=locals()[element](15)
    power_3.append(v3)
    power_5.append(v5)
    power_bat.append(vbat)
    if element=='Critical':
        print(element)
        print(v3)
        print(v5)
        print(vbat)



plt.figure(figsize=(19,10))
plt.title('Power Consumption in different Modes',fontsize=18)
plt.bar(mode,power_3,color="lightcoral",label="3.3V")
addlabels2(mode, power_3)
plt.bar(mode,power_5,color="red",bottom=np.array(power_3),label="5V")
addlabels(mode, power_5, power_3)
plt.bar(mode,power_bat,color="darkred",bottom=np.array(power_3)+np.array(power_5),label="Vbat")

plt.xticks(rotation=45,fontsize=12)
plt.yticks(fontsize=12)
plt.ylabel('Power in W',fontsize=15)
plt.xlabel('Power mode',fontsize=15)
plt.legend(loc="lower left",bbox_to_anchor=(0.8,1.0))
plt.subplots_adjust(bottom=0.22)
plt.show()

# t=0
# e_3=0
# e_5=0
# e_bat=0
# while t<150:
#     v5=0
#     v3=0
#     vbat=0
#     v3,v5,vbat=commissioning_test(t,0)
#     e_3=e_3+v3/60/60
#     e_5=e_5+v5/60/60
#     e_bat=e_bat+vbat/60/60
#     t=t+1
# print((e_bat+e_3+e_5))