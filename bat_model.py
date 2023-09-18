import math
import matplotlib.pyplot as plt
from variables import *


####################Batterie aging variables
t_a=[0]
cap=[Q]
R=[R_nom]
cfloat=[0]
a=2
b=-1.2
c=-0.0275   #default: -0.0275
t_cal_ref=3*365*24*60*60
T_0=23.5+273
T_bat=50+273
Tref=35+273
C_nom=Q

###################



QSoC=[Q_act[-1]]
SoC=[QSoC[-1]/Q*100]
Q_act[-1]=Q-Q_act[-1]       #Compute "empty battery charge"
Q_n=[Q]
Start_charge_decharge=[]    #Start charge = 1, start decharge = 2
swc=0                       #Start with charge or discharge cycle: charge = 3, discharge=2
DoD_calucalted=0            #Flag, that the DoD is just once calulated per cycle

#################### Battery aging function
def c_soc(t):
    return 1/(a+b*math.exp(c*(100-QSoC[-1])))

def c_float(t):
    try:
        temp= 1/t_cal_ref*t*1/(a+b*math.exp(c*(100-QSoC[-1]/C_nom*100)))* 2**((T_bat-T_0)/Tref)
        cfloat.append(temp)
        return temp
    except OverflowError:
        cfloat.append(cfloat[-1]) 
        return cfloat[-1] 

def resistance(t):
    return R_nom*(1+c_float(t))

def capacity(t):
    return C_nom*(1-0.2*(1-1+c_float(t)))

#Lithium Ion charge/discharge functions:
def f_discharge(it,i_f,i):
    f=E0-R[-1]*i-0.03125*K*Q/(Q-it)*i_f-0.75*K*Q/(Q-0.1*it)*it+A*math.exp(-B*it)
    return f
def f_charge(it,i_f,i):
    f=E0-R[-1]*i-0.0172*K*Q/(0.1*Q+it)*i_f-0.0172*K*Q/(Q-it)*it+A*math.exp(-B*it)
    return f

result_t=[0]
result_v=[]

charge_flag=0
discharge_flag=0
def charge_discharge(I,t):
    global charge_flag
    global discharge_flag
    global swc
    global DoD_calucalted
    global cycles

    # #Compute DoD:
    # if  DoD_calucalted==0 and len(Start_charge_decharge)%2==0 and len(Start_charge_decharge)>=2 and swc==2:
    #     t_startdischarge=Start_charge_decharge[-2][0]
    #     Q_startdischarge=QSoC[t_startdischarge]
    #     t_startcharge=Start_charge_decharge[-1][0]
    #     Qstartcharge=QSoC[t_startcharge]
    #     DoD.append((Q_startdischarge-Qstartcharge)/Q)
    #     cycles=cycles+1
    #     aging_factor(len(DoD))
    #     DoD_calucalted=1
    # if DoD_calucalted==0 and len(Start_charge_decharge)%2==1 and len(Start_charge_decharge)>=3 and swc==3:
    #     t_startdischarge=Start_charge_decharge[-2][0]
    #     Q_startdischarge=QSoC[t_startdischarge]
    #     t_startcharge=Start_charge_decharge[-1][0]
    #     Qstartcharge=QSoC[t_startcharge]
    #     DoD.append((Q_startdischarge-Qstartcharge)/Q)
    #     cycles=cycles+1
    #     aging_factor(len(DoD))
    #     DoD_calucalted=1
    #Initialization
    if I<0 and t==0:
        Start_charge_decharge.append((t,1))
        swc=3
        result_v.append(f_charge(Q_act[-1],I,I))
    elif I>0 and t==0:
        Start_charge_decharge.append((t,2))
        swc=2
        result_v.append(f_discharge(Q_act[-1],I,I))
    
    ###Charge model
    if I<0 and t>0:
        discharge_flag=0
        time=time_step/60/60
              
        #if QSoC[-1]-time*I<cap[-1]:
        
        if f_charge(Q_act[-1],I,I)<E0 or (QSoC[-1]-time*I)<0.99*Q:
            result_v.append(f_charge(Q_act[-1],I,I))
            Q_act.append(Q_act[-1]+time*I)
            QSoC.append(QSoC[-1]-time*I)
            if Start_charge_decharge[-1][1] == 2:
                Start_charge_decharge.append((t,1))
                DoD_calucalted=0
        elif charge_flag==0:
            charge_flag=1
            result_v.append(result_v[-1])
            QSoC.append(QSoC[-1])
            #print("Battery full, charging stopped with Q_act="+str(Q_act[-1]))
        else:
            result_v.append(result_v[-1])
            QSoC.append(QSoC[-1])
            #print("Charging stopped")
        SoC.append(QSoC[-1]/Q*100)   


    ###Working discharge model
    if I>0 and t>0:
        charge_flag=0
        time=time_step/60/60
             
        #if QSoC[-1]-time*I>0.09:
        if f_discharge(Q_act[-1],I,I)>battery_critical_voltage:    
            result_v.append(f_discharge(Q_act[-1],I,I))
            Q_act.append(Q_act[-1]+time*I+R[-1]*I*I*time)
            QSoC.append(QSoC[-1]-time*I-R[-1]*I*I*time)
            
            if Start_charge_decharge[-1][1] == 1:
                Start_charge_decharge.append((t,2))
                DoD_calucalted=0
        elif discharge_flag==0:
            discharge_flag=1
            result_v.append(result_v[-1])
            QSoC.append(QSoC[-1])
            #print("Battery empty, discharging stopped with Q_act="+str(Q_act[-1]))
        else:
            result_v.append(result_v[-1])
            QSoC.append(QSoC[-1])
            #print("Discharging stopped")
        SoC.append(QSoC[-1]/Q*100)

    if I==0:
        result_v.append(result_v[-1])
        QSoC.append(QSoC[-1])
        SoC.append(QSoC[-1]/Q*100)
        

    #battery aging
    if t>0:
        temp_cap=capacity(t)
        if temp_cap <= cap[-1]:
            cap.append(temp_cap)
        else:
            cap.append(cap[-1])

        temp_R=resistance(t)
        if temp_R >= R[-1]:
            R.append(temp_R)
        else:
            R.append(R[-1])
