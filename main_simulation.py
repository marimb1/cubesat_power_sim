from variables import *
from cubesat import *
from energy_harvesting import *
from subcomponents import *
from bat_model import *
from energy_harvesting import *
from datetime import datetime
from powermodes import *
from Orbit.orbit import orbit_calculation
from skyfield.api import utc
from os.path import exists
import csv
import math

#Read csv file:
#readfile()
print('Start')
#Create all components:
satellite = cubesat()


if do_orbit_simulation:
    print("Start orbit calculation")
    orbit_calculation(orbit_t_step,datetime(year,month,day,hour,minute,second,microsecond,utc),orbit_name,max_orbit_time,tle_file,csv_file_name_out_orbit)


print('Read orbit input file...')
#Read all Orbit data
with open('./Orbit/%s'%csv_file_to_use, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for idx,row in enumerate(reader):
        if idx==0:
            orbit_timestep=row[0]
            orbit_starttime=row[1]
        elif idx>0:
            orbit_time_sec.append(row[0])
            orbit_x_sat.append(row[1])
            orbit_y_sat.append(row[2])
            orbit_z_sat.append(row[3])
            orbit_sat_in_sun.append(row[4])
            orbit_earth_sun.append(row[5])
            orbit_sat_pos.append(row[6])
            orbit_sun_sat_pos.append(row[7])
            orbit_lat.append(row[8])
            orbit_lon.append(row[9])
            orbit_height.append(row[10])
print('Read orbit input file finished...')

#file variables
rotx=[satellite.rotational_speed_x[-1]]
roty=[satellite.rotational_speed_y[-1]]
rotz=[satellite.rotational_speed_z[-1]]
#Actual_power_mode="Tx"
next_mode=["Detumble"]
time_last_mode_change=0
time_last_tx=0
uhf_deployed=0
ready_to_test=0
ready_to_transmit=0
operational_mode=0
emergency=0
detumble_finished=0
W_use=[0]
Tx_window=[]
mode_at_T=["Detumble"]

 
#Initalization:
calculate_angles(0,satellite,1)
powerproduction_orbit(satellite,1)
charge_discharge(1,0)
transmition_window.append(check_for_transmition_window(1))
#Simulate satellite with timestep and maximum simulation time
day=1
t=1
while t <= max_simulation_time:
    if t>day*86400:
        print(day)
        day+=1

    #Add actual mode to array:
    mode_at_T.append(next_mode[-1])
    
    time_index=0
    for idx,element in enumerate(orbit_time_sec):
        if idx>0 and t<(float(element)+float(orbit_timestep)):
            time_index=idx
            break
    #Check for transmition window:
    transmition_window.append(check_for_transmition_window(time_index))
    #Activate charge mode at time 100: / Bring satellite in desired charging position
    if (next_mode[-1]=="Charge" or next_mode[-1]=="Experiment") and detumble_finished==1:
        charge_mode(satellite,[1,1,0],time_index)
    #powerproduction(t,satellite,time_index)
    powerproduction_orbit(satellite,time_index)
    #Calculate satellite position
    calculate_angles(t,satellite,time_index)
    calculate_satellite_angles(satellite)
    
    #Calculate degredation from solar panels (at different timepoints we can add a defect of a solar cell)
    if len(panel_defect)==0:
        solarpanel_degredation(t)
    else:
        if panel_defect[0][0]>t:
            solarpanel_degredation(t)
        else:
            solarpanel_degredation(t,panel_defect[0][1],panel_defect[0][2],panel_defect[0][3])
            panel_defect.pop(0)
    
    
    
    #Calculate powerproduction in current position
    
    #Calculate charge current considering actual battery voltage and mppt efficiency
    I_prod=-powerfrompanel(time_index)/result_v[-1]

    #I_use=total_consumption(all_subsystems,Actual_power_mode)/V_nom
    
    W_use_3_3=0
    W_use_5=0
    W_use_bat=0
    
    #Start Up satellite with detumbling mode
    if next_mode[-1]=="Detumble":
        W_use_3_3,W_use_5,W_use_bat=detumble(t,False)
        #Calculate new x speed:
        if (0<satellite.rotational_speed_x[-1] >=(rot_correction_speed_x*time_step+0.02)):
            satellite.rotational_speed_x.append(satellite.rotational_speed_x[-1]-rot_correction_speed_x*time_step)
        if -(rot_correction_speed_x*time_step+0.02)>=satellite.rotational_speed_x[-1]<0:
           satellite.rotational_speed_x.append(satellite.rotational_speed_x[-1]+rot_correction_speed_x*time_step)
        #Calculate new y speed:
        if (0<satellite.rotational_speed_y[-1] >=(rot_correction_speed_y*time_step+0.02)):
            satellite.rotational_speed_y.append(satellite.rotational_speed_y[-1]-rot_correction_speed_y*time_step)
        if -(rot_correction_speed_y*time_step+0.02)>=satellite.rotational_speed_y[-1]<0:
           satellite.rotational_speed_y.append(satellite.rotational_speed_y[-1]+rot_correction_speed_y*time_step)
        #Calculate new z speed:
        if (0<satellite.rotational_speed_z[-1] >=(rot_correction_speed_z*time_step+0.02)):
            satellite.rotational_speed_z.append(satellite.rotational_speed_z[-1]-rot_correction_speed_z*time_step)
        if -(rot_correction_speed_z*time_step+0.02)>=satellite.rotational_speed_z[-1]<0:
           satellite.rotational_speed_z.append(satellite.rotational_speed_z[-1]+rot_correction_speed_z*time_step)

        if (abs(satellite.rotational_speed_x[-1])>(rot_correction_speed_x*time_step+0.02) or abs(satellite.rotational_speed_y[-1])>(rot_correction_speed_y*time_step+0.02) or abs(satellite.rotational_speed_z[-1])>(rot_correction_speed_z*time_step+0.02)):
            next_mode.append("Detumble")
        else:
            detumble_finished=1
            next_mode.append("Charge")

    #Use power profile for corresponding profile
    match next_mode[-1]:
        case "DeployS":
            time_last_mode_change=t
            next_mode.append("Deploy")
        case "Deploy":
            W_use_3_3,W_use_5,W_use_bat=deploy(t)
        case "TestS":
            time_last_mode_change=t
            next_mode.append("Test")
            ready_to_test=0
        case "Test":
            W_use_3_3,W_use_5,W_use_bat=commissioning_test(t,time_last_mode_change)
        case "TxS_initial":
            next_mode.append("Tx_initial")
            W_use_3_3,W_use_5,W_use_bat=Tx_initial_round(t)
            ready_to_transmit=0
            time_last_mode_change=t
        case "Tx_initial":
            W_use_3_3,W_use_5,W_use_bat=Tx_initial_round(t)
        case "Charge":
            W_use_3_3,W_use_5,W_use_bat=Charge(t)
        case "Critical":
            W_use_3_3,W_use_5,W_use_bat=Critical(t)
        case "Emergency":
            W_use_3_3,W_use_5,W_use_bat=Emergency(t)
        case "GPS_scientific_S":
            time_last_mode_change=t
            W_use_3_3,W_use_5,W_use_bat=GNSS_positioning_scientific(t)
            next_mode.append("GPS_scientific")
        case "GPS_scientific":
            W_use_3_3,W_use_5,W_use_bat=GNSS_positioning_scientific(t)
        case "Experiment_S":
            W_use_3_3,W_use_5,W_use_bat=Experiment(t)
            next_mode.append("Experiment")
            time_last_mode_change=t
        case "Experiment":
            W_use_3_3,W_use_5,W_use_bat=Experiment(t)
        case "Split_S":
            W_use_3_3,W_use_5,W_use_bat=Split(t)
            next_mode.append("Split")
            time_last_mode_change=t
        case "Split":
            W_use_3_3,W_use_5,W_use_bat=Split(t)
        case "Rx_S":
            W_use_3_3,W_use_5,W_use_bat=RX_regular(t)
            next_mode.append("Rx")
            time_last_mode_change=t
            time_last_tx=t
        case "Rx":
            W_use_3_3,W_use_5,W_use_bat=RX_regular(t)
        case "Tx_S":
            W_use_3_3,W_use_5,W_use_bat=TX_regular(t)
            next_mode.append("Tx")
            time_last_mode_change=t
        case "Tx":
            W_use_3_3,W_use_5,W_use_bat=TX_regular(t)
        case "Free":
            W_use_3_3,W_use_5,W_use_bat=Charge(t)
            if operational_mode==0:
                next_mode.append("Charge")
        case "deploy_break":
             W_use_3_3,W_use_5,W_use_bat=Charge(t)


    #Charge if battery to low:
    if result_v[-1]<battery_critical_voltage*1.01 and next_mode[-1]!='Detumble':
        next_mode.append("Charge")
    # if result_v[-1]<battery_critical_voltage*1.01 and next_mode[-1]=='Detumble':
    #     next_mode.append("deploy_break")
    

    #check if Rx finished and start Tx
    if (((t-time_last_mode_change)>=Tx_time) and next_mode[-1]=="Rx"):
        next_mode.append("Tx_S")
    
    #check if Tx finished
    if (((t-time_last_mode_change)>=Tx_time) and next_mode[-1]=="Tx"):
        next_mode.append(next_mode[-5])

    #check if Tx test is finished       
    if (((t-time_last_mode_change)>=test_tx) and next_mode[-1]=="Tx_initial"):
        next_mode.append("Free")
        operational_mode=1
        ready_to_transmit=0

    #Check if Split is needed every 7 hours
    if (((t-time_last_mode_change)>=Split_time) and next_mode[-1]=="Experiment"):
        next_mode.append("Split_S")

    #Check if Split is finished
    if (((t-time_last_mode_change)>=Split_duration) and next_mode[-1]=="Split"):
        next_mode.append("Experiment_S")

    #check if GPS measurement is finished       
    if (((t-time_last_mode_change)>=GPS_measurement_duration) and next_mode[-1]=="GPS_scientific"):
        next_mode.append("Charge")
       

    #Check if ready for Tx test and if satellite is in position
    if ready_to_transmit==1 and check_for_transmition_window(time_index)==1:
        next_mode.append("TxS_initial")

    #Check if in operational mode and if satellite is in position for Tx
    if operational_mode==1 and check_for_transmition_window(time_index)==1 and result_v[-1]>battery_critical_voltage*1.2 and (t-time_last_tx)>1500:
        next_mode.append("Rx_S")


    #check if Commissioning test is finished       
    if (((t-time_last_mode_change)>=test_max_duration) and next_mode[-1]=="Test"):
        next_mode.append("Charge")
        ready_to_transmit=1


    #check if Deploy is finished       
    if (((t-time_last_mode_change)>deploy_max_duration) and next_mode[-1]=="Deploy"):
        next_mode.append("Charge")
        ready_to_test=1

    #Check if Satellte is ready to test in next round
    if ready_to_test==1 and SoC[-1]>50:
        next_mode.append("TestS")

    #Start deploy phase if not done already and with SoC enaugh high  
    if ((uhf_deployed==0) and (SoC[-1]>50) and (next_mode[-1]=="Charge")):
        next_mode.append("DeployS")
        uhf_deployed=1

    #Start GPS measuring every 15min
    if t%9000==0 and operational_mode==1:
        next_mode.append("GPS_scientific_S")

    #Start Experiment
    if operational_mode==1 and next_mode[-1]=="Free":
        next_mode.append("Experiment_S")

    if QSoC[-1]>0.98*Q and next_mode[-1]=='Charge':
        next_mode.append("Free")

    #Restart detumble:
    if(SoC[-1]<20 and detumble_finished==0):
        next_mode.append("Critical")
    if(SoC[-1]>80 and detumble_finished==0 and next_mode!="Detumble"):
        next_mode.append("Detumble")







    #Start Critical state
    if result_v[-1]<battery_critical_voltage:
        next_mode.append("Critical")
        emergency=1
        operational_mode=0
    if result_v[-1]<battery_emergency_voltage:
        next_mode.append("Emergency")
        emergency=2
        operational_mode=0
    if emergency==2 and result_v[-1]>battery_emergency_voltage*1.02:
        next_mode.append("Critical")
        emergency=1
    if emergency==1 and result_v[-1]>battery_critical_voltage*1.2:
        next_mode.append("Charge")
        emergency=0
        operational_mode=1
    

    #Calculate Powerconsumption from battery
    W_use_3_3_eff=W_use_3_3/get_efficiency(3.3,W_use_3_3/3.3)
    W_use_5_eff=W_use_5/get_efficiency(5,W_use_5/5)
    W_use_tot=W_use_bat+W_use_5_eff+W_use_3_3_eff
    W_use.append(W_use_tot)
    I_use=W_use_tot/result_v[-1]
    I_tot=I_prod+I_use

    #Update battery state:
    charge_discharge(I_tot,t)

    #Go to next iteration
    result_t.append(t)
    t+=time_step
    rotx.append(satellite.rotational_speed_x[-1])
    roty.append(satellite.rotational_speed_y[-1])
    rotz.append(satellite.rotational_speed_z[-1])




#Change next mode:
for idx,element in enumerate(mode_at_T):
    if element == 'Tx_S':
        mode_at_T[idx]='Tx'
    if element == 'GPS_S':
        mode_at_T[idx]='GPS'
    if element == 'Rx_S':
        mode_at_T[idx]='Rx'
    if element == 'Experiment_S':
        mode_at_T[idx]='Experiment'
    if element == 'DeployS':
        mode_at_T[idx]='Deploy'
    if element == 'TestS':
        mode_at_T[idx]='Test'
    if element == 'TxS_initial':
        mode_at_T[idx]='Tx_initial'
    if element == 'GPS_scientific_S':
        mode_at_T[idx]='GPS_scientific'
    if element == 'Split_S':
        mode_at_T[idx]='Split'

#Create csv file with output data:
i=1
o_path='./simulation_output/%s.csv'%str(i)
while (exists(o_path)):
    i+=1
    o_path='./simulation_output/%s.csv'%str(i)
    
print('Write output file with name %s.csv'%str(i))
with open(o_path, 'w',newline='') as file:
    writer = csv.writer(file)
    writer.writerow(result_t)
    writer.writerow(result_v)
    writer.writerow(Q_act)
    writer.writerow(QSoC)
    writer.writerow(SoC)
    writer.writerow(panel1_power)
    writer.writerow(panel2_power)
    writer.writerow(panel3_power)
    writer.writerow(panel_all_power)
    writer.writerow(cap)
    writer.writerow(mode_at_T)
    writer.writerow(W_use)
    writer.writerow(transmition_window)
    writer.writerow(rotx)
    writer.writerow(roty)
    writer.writerow(rotz)

# plt.plot(result_t,result_v,'.')
# #plt.subplot(result_t,Q_act, '.')
# plt.title("CHARGE CURVE")
# plt.xlabel("time in s")
# plt.ylabel("Battery Voltage in V")
# plt.show()
# plt.plot(result_t,QSoC)
# plt.xlabel("time in s")
# plt.ylabel("Battery state of charge in Ah")
# plt.show()
# plt.plot(result_t,SoC)
# plt.xlabel("time in s")
# plt.ylabel("Battery state of charge in %")
# plt.show()
# plt.plot(result_t,cap)
# plt.xlabel("time in s")
# plt.ylabel("capacity over time")
# plt.show()
# plt.subplot(2,1,1)
# plt.plot(result_t,powerproduction_factor_panel1,label="Panel 1")
# plt.plot(result_t,powerproduction_factor_panel2,label="Panel 2")
# plt.plot(result_t,powerproduction_factor_panel3,label="Panel 3")
# plt.legend()
# plt.subplot(2,1,2)
# plt.plot(result_t,satellite.angle_x)
# plt.plot(result_t,satellite.angle_y)
# plt.plot(result_t,satellite.angle_z)
# plt.show()
# plt.plot(result_t,panel1_power,label="Panel 1")
# plt.plot(result_t,panel2_power,label="Panel 2")
# plt.plot(result_t,panel3_power,label="Panel 3")
# plt.plot(result_t,panel_all_power,label="Total")
# plt.legend()
# plt.title("Power Production of all panels")
# plt.xlabel("time in s")
# plt.ylabel("Power")
# plt.show()



# plt.plot(result_t,W_use,'.')
# plt.title("Power Consumption in W")
# plt.xlabel("time in s")
# plt.ylabel("W")
# plt.show()

# plt.plot(result_t,mode_at_T,'.')
# plt.title("Active Power Mode")
# plt.xlabel("time in s")
# plt.ylabel("Power Mode")
# plt.show()


# print(powerproduction_factor_panel1)
# print(satellite.angle_x)
# print(satellite.angle_y)
# print(satellite.angle_z)
# print(satellite.angle_to_sun)




plt.subplot(3,1,1)
plt.plot(result_t,panel1_power,label="Panel 1")
plt.plot(result_t,panel2_power,label="Panel 2")
plt.plot(result_t,panel3_power,label="Panel 3")
plt.plot(result_t,panel_all_power,label="Total")
plt.legend()
plt.title("Power Production of all panels")
plt.xlabel("time in s")
plt.ylabel("Power")

plt.subplot(3,1,2)
plt.plot(result_t,mode_at_T,'.')
plt.title("Active Power Mode")
plt.xlabel("time in s")
plt.ylabel("Power Mode")

plt.subplot(3,1,3)
plt.plot(result_t,W_use,'.')
plt.title("Power Consumption in W")
plt.xlabel("time in s")
plt.ylabel("W")

plt.subplots_adjust(hspace=0.6)
plt.show()

plt.plot(result_t,SoC)
plt.title('Battery SoC')
plt.xlabel('Time [s]')
plt.ylabel('SoC [%]')
plt.show()


# fig, ax1=plt.subplots()

# color='tab:red'
# ax1.set_xlabel('time (s)')
# ax1.set_ylabel('Battery Voltage', color=color)
# ax1.plot(result_t, result_v, color=color)
# ax1.tick_params(axis='y', labelcolor=color)

# ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

# color = 'tab:blue'
# ax2.set_ylabel('SoC in %', color=color)  # we already handled the x-label with ax1
# ax2.plot(result_t, SoC, color=color)
# ax2.tick_params(axis='y', labelcolor=color)
# plt.show()
# #plt.tight_layout()  # otherwise the right y-label is slightly clipped

# plt.plot(result_t,panel1_power,label="Panel 1")
# plt.plot(result_t,panel2_power,label="Panel 2")
# plt.plot(result_t,panel3_power,label="Panel 3")
# plt.plot(result_t,panel_all_power,label="Total")
# plt.legend()
# plt.title("Power Production of all panels")
# plt.xlabel("time in s")
# plt.ylabel("Power")
# plt.show()



# ax = plt.figure().add_subplot(projection='3d')
# ax.scatter(satellite.orbit_x, satellite.orbit_y, satellite.orbit_z, label='Satellite Orbit')
# ax.legend()


# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')

# ax.view_init(elev=20., azim=-35, roll=0)

# plt.show()
# list=[]
# for idx,element in enumerate(px1b):
#     list.append(px1b[idx]+py1b[idx]+pz1b[idx])
# plt.subplot(3,1,1)
# plt.plot(result_t,px1b,label='1')
# plt.plot(result_t,py1b,label='2')
# plt.plot(result_t,pz1b,label='3')
# plt.plot(result_t,list,label='1+2')
# plt.legend()
# plt.subplot(3,1,2)
# plt.plot(result_t,mode_at_T)

# plt.subplot(3,1,3)
# plt.plot(result_t,anglex1test,label='Angle Z')
# plt.plot(result_t,anglehtest,label='XY')
# plt.legend()
# plt.show()
time_hours=[i/60/60 for i in result_t]
plt.plot(time_hours,transmition_window)
plt.title('Transmission window')
plt.xlabel('Time [h]')
plt.ylabel('Data Transmission')
plt.show()