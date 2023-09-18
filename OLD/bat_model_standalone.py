import math
import matplotlib.pyplot as plt

#################### given Variables
V_nom=3.3           #V
I_in=-2              #A (Positive=discharge)
E0=3.366            #Constant voltage
K=0.0076            #(nom Voltage / nominal Capacity)
Q=2.3               #Max capacity
Q_act=0.09          #Integrated Current (Ah) (Actual battery charge)
A=0.264             #Exponential zone variable       
B=26.54             #Exponential zone variable
R=0.01              #Internal resistance
####################
Q_act=Q-Q_act       #Compute "empty battery charge"
Q_n=[Q]
Epsilon=[0]
DoD=[80,80,80]
#################### Battery aging functions
def aging_factor(n):
    E_new=Epsilon[-1]+0.5/(120000*(n-1))*(2-(DoD[-3]*DoD[-1])/DoD[-2])
    Epsilon.append(E_new)

#Lithium Ion charge/discharge functions:
def f_discharge(it,i_f,i):
    f=E0-R*i-K*Q/(Q-it)*i_f-K*Q/(Q-it)*it+A*math.exp(-B*it)
    return f
def f_charge(it,i_f,i):
    f=E0-R*i-K*Q/(0.1*Q+it)*i_f-K*Q/(Q-it)*it+A*math.exp(-B*it)
    return f

result_t=[]
result_v=[]
t=0
I=I_in

###Charge model
while True:
    time=1/60/60
    Q_act+=time*I
    # if Q_act<0:
    #     break
    result_t.append(t)
    result_v.append(f_charge(Q_act,I,I))
    if result_v[-1]>4:
        break
    t+=1

###Working discharge model
while True:
    time=1/60/60
    Q_act+=time*I
    #if Q_act>2.2:
    #    break
    result_t.append(t)
    result_v.append(f_discharge(Q_act,I,I))
    if result_v[-1]<2.95:
        break
    t+=1

plt.plot(result_t,result_v)
plt.title("CHARGE CURVE")
plt.xlabel("time in s")
plt.ylabel("Battery Voltage in V")
plt.show()