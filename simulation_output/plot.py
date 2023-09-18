import csv
import matplotlib.pyplot as plt


result_t=[]
result_v=[]
Q_act=[]
QSoC=[]
SoC=[]
panel1_power=[]
panel2_power=[]
panel3_power=[]
panel_all_power=[]
cap=[]
mode_at_T=[]
W_use=[]
transmition_window=[]
rotx=[]
roty=[]
rotz=[]

with open('./experiment.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    i=0
    for row in reader:
        if i==0:
            r=[float(i) for i in row ]
            result_t=r
        if i==1:
            r=[float(i) for i in row ]
            result_v=r
        if i==2:
            r=[float(i) for i in row ]
            Q_act=r
        if i==3:
            r=[float(i) for i in row ]
            QSoC=r
        if i==4:
            r=[float(i) for i in row ]
            SoC=r
        if i==5:
            r=[float(i) for i in row ]
            panel1_power=r
        if i==6:
            r=[float(i) for i in row ]
            panel2_power=r
        if i==7:
            r=[float(i) for i in row ]
            panel3_power=r
        if i==8:
            r=[float(i) for i in row ]
            panel_all_power=r
        if i==9:
            r=[float(i) for i in row ]
            cap=r
        if i==10:
            mode_at_T=row
        if i==11:
            r=[float(i) for i in row ]
            W_use=r
        if i==12:
            r=[float(i) for i in row ]
            transmition_window=r
        if i==13:
            r=[float(i) for i in row ]
            rotx=r
        if i==14:
            r=[float(i) for i in row ]
            roty=r
        if i==15:
            r=[float(i) for i in row ]
            rotz=r
        i+=1
time_h=[i/60/60 for i in result_t]
durchschnitt=sum(panel_all_power)/len(panel_all_power)
durch=[durchschnitt for i in result_t]

durchschnitt_verb=sum(W_use)/len(W_use)
verb=[durchschnitt_verb for i in result_t]


plt.figure(figsize=(10,6))
plt.subplot(3,1,1)
plt.plot(time_h,mode_at_T,'.')
plt.xticks(fontsize=0)
plt.yticks(fontsize=11)

plt.ylabel('Active Power Mode',fontsize=13,labelpad=20)



plt.subplot(3,1,2)
plt.plot(time_h,panel_all_power,label='Power production',color='forestgreen')
plt.plot(time_h,durch,label='Average production',color='limegreen')
plt.plot(time_h,W_use,label='Power consumption',color='tomato')

#plt.plot(time_h,durch,label='Average consumption')
plt.xticks(fontsize=0)
plt.yticks(range(0,26,5),fontsize=11)
plt.ylabel('Power [W]',fontsize=13,labelpad=30)


plt.legend(loc='upper right')



plt.subplot(3,1,3)
plt.plot(time_h,SoC)
plt.xticks(fontsize=13)
plt.yticks(fontsize=11)
plt.xlabel('Time [h]',fontsize=15)
plt.ylabel('State of Charge [%]',fontsize=13)
plt.subplots_adjust(left=0.175)
plt.savefig('subplot_experiment_aa4.pdf')
plt.show()




#Power Production and consumption
plt.plot(time_h[1000:1200],panel_all_power[1000:1200],label='Power production',color='forestgreen')
plt.plot(time_h[1000:1200],durch[1000:1200],label='Average production',color='limegreen')
plt.plot(time_h[1000:1200],W_use[1000:1200],label='Power consumption',color='tomato')

plt.yticks(range(0,13,2),fontsize=11)
plt.xticks(fontsize=11)
plt.xlabel('Time [h]',fontsize=13)
plt.ylabel('Power [W]',fontsize=13)
plt.legend()
# plt.title('Power Production and Consumption')
plt.savefig('energy_harvesting.pdf')
plt.show()



fig,ax=plt.subplots(figsize=(10,6))
ax.plot(time_h,panel_all_power,label='Power production',color='forestgreen')
ax.plot(time_h,durch,label='Average power production',color='lime')
ax.plot(time_h,W_use,label='Power consumption',color='tomato')



ax.set_xlabel('Time [h]',fontsize=15)
ax.set_xticklabels(ax.get_xticklabels(),fontsize=12)
ax.set_yticklabels(ax.get_yticklabels(),fontsize=12)
ax.set_ylabel('Power [W]',fontsize=15)
axins=ax.inset_axes([0.1, 1.2, 0.5, 0.5])
axins.plot(time_h,panel_all_power,color='forestgreen')
axins.plot(time_h,W_use,color='tomato')
axins.plot(time_h,durch,color='lime')
axins.set_xlim(10,11)
axins.set_xlabel('Time [h]')
axins.set_ylabel('Power [W]')
axins.set_ylim(-0.5,10)
ax.indicate_inset_zoom(axins,edgecolor='black')
plt.subplots_adjust(top=0.6)
plt.legend(loc='upper right', bbox_to_anchor=(1, 1.55))
plt.title('Power Production and Consumption')
plt.savefig('Power_detumbling_together_2.pdf')
plt.show()


# plt.ylabel('Transmission window open',fontsize=13)
# plt.xlabel('Time [h]',fontsize=13)
# plt.xticks(fontsize=11)
# plt.yticks([0,1],fontsize=11)
# plt.show()


#Plot transmission window
# fig,ax=plt.subplots(figsize=(10,6))
# ax.plot(time_h,transmition_window)
# ax.set_xlabel('Time [h]',fontsize=13)
# ax.set_ylabel('Transmission window',fontsize=13)
# ax.set_yticks([0,1])
# axins=ax.inset_axes([0, 1.2, 1, 0.5])
# axins.plot(time_h,transmition_window)
# axins.set_xlim(28,38.5)
# axins.set_xlabel('Time [h]')
# axins.set_ylabel('Transmission window')
# axins.set_yticks([0,1])
# axins.set_ylim(-0.05,1.05)
# ax.indicate_inset_zoom(axins,edgecolor='black')
# plt.subplots_adjust(top=0.6)
# plt.savefig('transmission_window.pdf')
# plt.show()

plt.plot(time_h[1000:1200],panel_all_power[1000:1200],label='Power production',color='forestgreen')
plt.plot(time_h[1000:1200],durch[1000:1200],label='Average production',color='limegreen')
plt.plot(time_h[1000:1200],W_use[1000:1200],label='Power consumption',color='tomato')
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)
plt.xlabel('Time [h]',fontsize=13)
plt.ylabel('Power [W]',fontsize=13)
plt.subplots_adjust(left=0.175)
plt.show()