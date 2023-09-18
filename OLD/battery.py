from variables import initial_capcity
from variables import max_charge_current
from variables import max_decharge_current
from variables import battery_initial_voltage
from variables import battery_initial_state_of_charge
from variables import time_step

#Variables for battery Algorithms
E0=4.2      #Battery constant voltage
R=0.021     #Internal resistance in Ohm


#Calculate Watthours from watt and timestep
def watthours(watt):
    return watt*time_step/3600

class battery:
    def __init__(self):
        self.capacity=initial_capcity
        self.max_charge_current=max_charge_current
        self.max_decharge_current=max_decharge_current
        self.battery_degredation_array=[0]
        self.battery_temperature=[0]
        self.capacity_including_degredation=[initial_capcity]
        self.charge_current=[0]
        self.decharge_current=[0]
        self.battery_voltage=[battery_initial_voltage]
        self.state_of_charge=[battery_initial_state_of_charge]

    def add_values(self,capacity_degredation,charge_current,decharge_current,state_of_charge,battery_temperature):
        self.battery_temperature.append(battery_temperature)
        self.capacity_including_degredation.append(capacity_degredation)
        self.charge_current.append(charge_current)
        self.decharge_current.append(decharge_current)
        #self.battery_voltage.append(battery_voltage)
        self.state_of_charge.append(state_of_charge)

    def battery_degredation(self,age,temperature):
        deg=self.battery_degredation_array[-1]+age*0.001
        if deg >=100:
            deg=100
        self.battery_degredation_array.append(deg)

    def charge_decharge(self, t,chargepower,dechargepower):
        new_state_of_charge=self.state_of_charge[-1]
        new_battery_voltage=0
        if(chargepower>dechargepower):
            #charging mode
            new_battery_voltage=0
        else:
            #decharging mode
            charging=watthours(chargepower)
            decharging=watthours(dechargepower)
            
