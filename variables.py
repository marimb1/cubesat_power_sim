
####################################################################################################
###Define variables for power simulation
time_step = 60                      #in seconds
max_simulation_time = 2*24*60*60        #in seconds
####################################################################################################

####################################################################################################
####Battery variables from datasheet
Cells_in_Serie=4
E0=Cells_in_Serie*3.95           #Constant voltage
K=0.45                           #( Voltage /  Capacity)
Q=Cells_in_Serie*2.035           #Max capacity
Q_act=[Cells_in_Serie*2.034]     #Integrated Current (Ah) (Actual battery charge)
A=Cells_in_Serie*0.1             #Exponential zone variable       
B=Cells_in_Serie*100             #Exponential zone variable
R_nom=0.025/Cells_in_Serie       #Internal resistance
battery_critical_voltage=Cells_in_Serie*2.85
battery_emergency_voltage=Cells_in_Serie*2.75
####################################################################################################

####################################################################################################
###Orbit Simulation
do_orbit_simulation=True
orbit_t_step=60
year=2023
month=6
day=4
hour=5
minute=7
second=0
microsecond=0
max_orbit_time=2*24*60*60
tle_file = './Orbit/orbit_tle.txt'
orbit_name= 'AAUSAT-4'
csv_file_name_out_orbit='orbit_2_days_aausat_presentation.csv'         #new csv file
csv_file_to_use='orbit_2_days_aausat_presentation.csv'
####################################################################################################



####################################################################################################
###Ground Station
ground_station_lon=8.55         #in grad
ground_station_lat=47.366       #in grad
ground_station_radius=20        #in grad
####################################################################################################

####################################################################################################
###Cubsate angles initial value
angle_1=0       #in grad
angle_2=0       #in grad
angle_3=0       #in grad

###Initial rotational speed
rotational_speed_x=0        #grad per second
rotational_speed_y=0        #grad per second
rotational_speed_z=0        #grad per second

###Rotational correction speed
rot_correction_speed_x=0.000001     #grad per second
rot_correction_speed_y=0.000001     #grad per second
rot_correction_speed_z=0.000001     #grad per second
####################################################################################################


####################################################################################################
###Solarpanel data
solarpanel_1_power=8    #Watt
solarpanel_2_power=8    #Watt
solarpanel_3_power=8    #Watt
###Set inital health of Panel, 1=100% new
health_panel1=[1]       #Initial health
health_panel2=[1]       #Initial health
health_panel3=[1]       #Initial health
panel_defect=[(2000,0,0.7,0)]         #defects of panel a is a list the form [(time,panel1_percent_defect,panel2_percent_defect,panel3_percent_defect)]
####################################################################################################


####################################################################################################
###Set durations of operations
deploy_max_duration=120         #seconds
test_max_duration=149           #seconds
test_tx=300                     #seconds
GPS_measurement_duration=60     #seconds

#Experiment
Split_time=6*60*60
Split_duration=180

#Transimssion
Tx_time=60*7     #seconds
Rx_time=10     #seconds
####################################################################################################








####################################################################################################
###DO NOT CHANGE VARIABLES BELOW HERE
####################################################################################################
orbit_starttime=0
orbit_timestep=0
orbit_time_sec=[]
orbit_x_sat=[]
orbit_y_sat=[]
orbit_z_sat=[]
orbit_sat_in_sun=[]
orbit_earth_sun=[]
orbit_sat_pos=[]
orbit_sun_sat_pos=[]
orbit_lat=[]
orbit_lon=[]
orbit_height=[]

panel1_power=[0]
panel2_power=[0]
panel3_power=[0]
panel_all_power=[0]

transmition_window=[]