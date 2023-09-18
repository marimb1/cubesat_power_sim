import math
import matplotlib.pyplot as plt

SoC=[0]
t_a=[0]
cap=[2.3]
R=[0.01]
cfloat=[0]
a=2
b=-1.2
c=-0.0275   #default: -0.0275

t_cal_ref=2*365*24*60*60
T_0=23.5+273
T_bat=50+273
Tref=35+273
C_nom=2.3
R_nom=0.01

def c_soc(t):
    return 1/(a+b*math.exp(c*(100-SoC[-1])))

def c_float(t):
    temp= 1/t_cal_ref*t*1/(a+b*math.exp(c*(100-SoC[-1]/cap[-1]*100)))* 2**((T_bat-T_0)/Tref)
    cfloat.append(temp) 
    return temp 

def resistance(t):
    return R_nom*(1+c_float(t))

def capacity(t):
    return C_nom*(1-0.2*(1-1+c_float(t)))

Ah_ps=2/60/60
t=0
while t < 365*24*60*60:
    for i in range(0,6000):
        if SoC[-1]+Ah_ps < cap[-1]:
            SoC.append((SoC[-1]+Ah_ps))
        else:
            SoC.append(SoC[-1])

        t_a.append(t)
        t+=1
        cap.append(capacity(t))
        R.append(resistance(t))

    for i in range(0,1000):
        if SoC[-1]-Ah_ps>0:
            SoC.append((SoC[-1]-Ah_ps))
        else:
            SoC.append(SoC[-1])

        t_a.append(t)
        t+=1
        cap.append(capacity(t))
        R.append(resistance(t))

list=[i/C_nom*100 for i in SoC]
plt.plot(t_a,list)
plt.title("actual charging/decharging curve")
plt.xlabel("time in seconds")
plt.ylabel("Capacity in Ah")
plt.show()

# plt.plot(t_a,cap)
# plt.title("Maximum capacity of battery over life")
# plt.xlabel("time in seconds")
# plt.ylabel("Capacity in Ah")
# plt.show()
print(cap[-1])
print(R[-1])