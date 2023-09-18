from subcomponents import *
from variables import orbit_x_sat,orbit_y_sat,orbit_z_sat
from detumble_initial_values import set_initial_rotational_speed
import math

def charge_mode(cubesat,activepanels,idx):
    #Panel 1 and should be active (target angles: x=0,y=0,z=45, z_rot)
    if activepanels[0]==1 and activepanels[1]==1:
        cubesat.rotational_speed_x.append(0)
        cubesat.rotational_speed_y.append(0)
        cubesat.rotational_speed_z.append(0)
        #cubesat.rotational_speed_z[-1]=cubesat.angle_to_sun[-1]-cubesat.angle_to_sun[-2]
        x=cubesat.orbit_x[-1]
        y=cubesat.orbit_y[-1]
        z=cubesat.orbit_z[-1]
        # cubesat.angle_x[-1]=0
        # cubesat.angle_y[-1]=0
        # cubesat.angle_z[-1]=cubesat.angle_to_sun[-1]-45
        dist=math.sqrt(float(orbit_x_sat[idx])**2+float(orbit_y_sat[idx])**2+float(orbit_z_sat[idx])**2)
        angle_xy=math.tan(x/y)
        angle_h=math.cos((math.sqrt(float(orbit_x_sat[idx])**2+float(orbit_y_sat[idx])**2))/dist)

        cubesat.angle_x[-1]=angle_h
        cubesat.angle_y[-1]=angle_h
        cubesat.angle_z[-1]=angle_xy-45


        

    if activepanels[0]==1 and activepanels[2]==1:
        cubesat.rotational_speed_x.append(0)
        cubesat.rotational_speed_y.append(0)
        cubesat.rotational_speed_z.append(0)
        #cubesat.rotational_speed_z[-1]=cubesat.angle_to_sun[-1]-cubesat.angle_to_sun[-2]
        x=cubesat.orbit_x[-1]
        y=cubesat.orbit_y[-1]
        z=cubesat.orbit_z[-1]
        # cubesat.angle_x[-1]=0
        # cubesat.angle_y[-1]=0
        # cubesat.angle_z[-1]=cubesat.angle_to_sun[-1]-45
        dist=math.sqrt(float(orbit_x_sat[idx])**2+float(orbit_y_sat[idx])**2+float(orbit_z_sat[idx])**2)
        angle_xy=math.tan(x/y)
        angle_h=math.cos((math.sqrt(float(orbit_x_sat[idx])**2+float(orbit_y_sat[idx])**2))/dist)

        cubesat.angle_x[-1]=angle_h
        cubesat.angle_y[-1]=angle_h
        cubesat.angle_z[-1]=angle_xy+45

#Input: simulation time and bool random initial speed should be enabled
#Output Power consumption in Wh for mode detumble
def detumble(time,random_speed=False):
    #Calculate starting rotational speed
    if random_speed==True:
        set_initial_rotational_speed()
    power_3_3=0
    power_5=0

    power_reaction_wheels=0
    if time in range(0,10):
        power_reaction_wheels=ADCS_reactionweheels.powerconsumption["max_torque"]*ADCS_reactionweheels.number_included
    else:
        power_reaction_wheels=ADCS_reactionweheels.powerconsumption["average"]*ADCS_reactionweheels.number_included

    power_gnss=ADCS_GNSS_system.powerconsumption["idle"]*ADCS_GNSS_system.number_included
    power_magentorquer=ADCS_magnetorquer.powerconsumption["peak"]*ADCS_magnetorquer.number_included
    power_sunsensor=ADCS_sunsensor.powerconsumption["idle"]*ADCS_sunsensor.number_included
    power_magnetometer=ADCS_magnetometer.powerconsumption["ultra_high_res"]*ADCS_magnetometer.number_included
    power_IMU=ADCS_imu.powerconsumption["gyroscope_accelerometer_normal"]*ADCS_imu.number_included
    power_satnogs = COM_satnogs_board.powerconsumption["idle"]*COM_satnogs_board.number_included
    power_amateur=COM_amateur_radio.powerconsumption["idle"]*COM_amateur_radio.number_included
    power_eps=EPS_battery_board.powerconsumption["always"]*EPS_battery_board.number_included
    power_eps_solar=EPS_solarpanel.powerconsumption["idle"]*EPS_solarpanel.number_included
    power_obc=OBC_board.powerconsumption["always"]*OBC_board.number_included
    power_pay=PAY_all.powerconsumption["idle"]*PAY_all.number_included


    power_3_3=power_gnss+power_magentorquer+power_sunsensor+power_magnetometer+power_IMU+power_obc
    power_5=power_reaction_wheels+power_satnogs+power_amateur+power_eps_solar+power_pay
    power_from_bat=power_eps

    return power_3_3,power_5,power_from_bat

#Input: simulation time
#Output Power consumption in Wh for mode deploy
def deploy(time):
    power_3_3=0
    power_5=0

    power_reaction_wheels=ADCS_reactionweheels.powerconsumption["idle"]*ADCS_reactionweheels.number_included
    power_gnss=ADCS_GNSS_system.powerconsumption["idle"]*ADCS_GNSS_system.number_included
    power_magentorquer=ADCS_magnetorquer.powerconsumption["idle"]*ADCS_magnetorquer.number_included
    power_sunsensor=ADCS_sunsensor.powerconsumption["idle"]*ADCS_sunsensor.number_included
    power_magnetometer=ADCS_magnetometer.powerconsumption["ultra_high_res"]*ADCS_magnetometer.number_included
    power_IMU=ADCS_imu.powerconsumption["gyroscope_accelerometer_normal"]*ADCS_imu.number_included
    power_satnogs = COM_satnogs_board.powerconsumption["deploy"]*COM_satnogs_board.number_included
    power_amateur=COM_amateur_radio.powerconsumption["idle"]*COM_amateur_radio.number_included
    power_eps=EPS_battery_board.powerconsumption["always"]*EPS_battery_board.number_included
    power_eps_solar=EPS_solarpanel.powerconsumption["idle"]*EPS_solarpanel.number_included
    power_obc=OBC_board.powerconsumption["always"]*OBC_board.number_included
    power_pay=PAY_all.powerconsumption["idle"]*PAY_all.number_included


    power_3_3=power_gnss+power_magentorquer+power_sunsensor+power_magnetometer+power_IMU+power_obc
    power_5=power_reaction_wheels+power_satnogs+power_amateur+power_eps_solar+power_pay
    power_from_bat=power_eps

    return power_3_3,power_5,power_from_bat

#Input: simulation time and time when entering this mode
#Output Power consumption in Wh for mode commissioning test, go over all components and look if they work.
def commissioning_test(time,last_mode):

    testseconds=time-last_mode

    power_3_3=0
    power_5=0
    test_nr=0
    if testseconds in range(0,10):
        test_nr=1
    elif testseconds in range(10,20):
        test_nr=2
    elif testseconds in range(20,50):
        test_nr=3
    elif testseconds in range(50,60):
        test_nr=4
    elif testseconds in range(60,70):
        test_nr=5
    elif testseconds in range(70,80):
        test_nr=6
    elif testseconds in range(80,90):
        test_nr=7
    elif testseconds in range(100,110):
        test_nr=8
    elif testseconds in range(110,120):
        test_nr=9
    elif testseconds in range(120,130):
        test_nr=10
    elif testseconds in range(130,140):
        test_nr=11
    elif testseconds in range(140,150):
        test_nr=12
    else:
        test_nr=1

    match test_nr:
        case 1:
            power_reaction_wheels=ADCS_reactionweheels.powerconsumption["max_torque"]*ADCS_reactionweheels.number_included
            power_gnss=ADCS_GNSS_system.powerconsumption["idle"]*ADCS_GNSS_system.number_included
            power_magentorquer=ADCS_magnetorquer.powerconsumption["idle"]*ADCS_magnetorquer.number_included
            power_sunsensor=ADCS_sunsensor.powerconsumption["idle"]*ADCS_sunsensor.number_included
            power_magnetometer=ADCS_magnetometer.powerconsumption["idle"]*ADCS_magnetometer.number_included
            power_IMU=ADCS_imu.powerconsumption["idle"]*ADCS_imu.number_included
            power_satnogs = COM_satnogs_board.powerconsumption["idle"]*COM_satnogs_board.number_included
            power_amateur=COM_amateur_radio.powerconsumption["idle"]*COM_amateur_radio.number_included
            power_pay=PAY_all.powerconsumption["idle"]*PAY_all.number_included
        case 2:
            power_reaction_wheels=ADCS_reactionweheels.powerconsumption["average"]*ADCS_reactionweheels.number_included
            power_gnss=ADCS_GNSS_system.powerconsumption["idle"]*ADCS_GNSS_system.number_included
            power_magentorquer=ADCS_magnetorquer.powerconsumption["idle"]*ADCS_magnetorquer.number_included
            power_sunsensor=ADCS_sunsensor.powerconsumption["idle"]*ADCS_sunsensor.number_included
            power_magnetometer=ADCS_magnetometer.powerconsumption["idle"]*ADCS_magnetometer.number_included
            power_IMU=ADCS_imu.powerconsumption["idle"]*ADCS_imu.number_included
            power_satnogs = COM_satnogs_board.powerconsumption["idle"]*COM_satnogs_board.number_included
            power_amateur=COM_amateur_radio.powerconsumption["idle"]*COM_amateur_radio.number_included
            power_pay=PAY_all.powerconsumption["idle"]*PAY_all.number_included

        case 3:
            power_reaction_wheels=ADCS_reactionweheels.powerconsumption["idle"]*ADCS_reactionweheels.number_included
            power_gnss=ADCS_GNSS_system.powerconsumption["scientific_mode"]*ADCS_GNSS_system.number_included
            power_magentorquer=ADCS_magnetorquer.powerconsumption["idle"]*ADCS_magnetorquer.number_included
            power_sunsensor=ADCS_sunsensor.powerconsumption["idle"]*ADCS_sunsensor.number_included
            power_magnetometer=ADCS_magnetometer.powerconsumption["idle"]*ADCS_magnetometer.number_included
            power_IMU=ADCS_imu.powerconsumption["idle"]*ADCS_imu.number_included
            power_satnogs = COM_satnogs_board.powerconsumption["idle"]*COM_satnogs_board.number_included
            power_amateur=COM_amateur_radio.powerconsumption["idle"]*COM_amateur_radio.number_included
            power_pay=PAY_all.powerconsumption["idle"]*PAY_all.number_included
           
        case 4:
            power_reaction_wheels=ADCS_reactionweheels.powerconsumption["idle"]*ADCS_reactionweheels.number_included
            power_gnss=ADCS_GNSS_system.powerconsumption["idle"]*ADCS_GNSS_system.number_included
            power_magentorquer=ADCS_magnetorquer.powerconsumption["peak"]*ADCS_magnetorquer.number_included
            power_sunsensor=ADCS_sunsensor.powerconsumption["idle"]*ADCS_sunsensor.number_included
            power_magnetometer=ADCS_magnetometer.powerconsumption["idle"]*ADCS_magnetometer.number_included
            power_IMU=ADCS_imu.powerconsumption["idle"]*ADCS_imu.number_included
            power_satnogs = COM_satnogs_board.powerconsumption["idle"]*COM_satnogs_board.number_included
            power_amateur=COM_amateur_radio.powerconsumption["idle"]*COM_amateur_radio.number_included
            power_pay=PAY_all.powerconsumption["idle"]*PAY_all.number_included
            
        case 5:
            power_reaction_wheels=ADCS_reactionweheels.powerconsumption["idle"]*ADCS_reactionweheels.number_included
            power_gnss=ADCS_GNSS_system.powerconsumption["idle"]*ADCS_GNSS_system.number_included
            power_magentorquer=ADCS_magnetorquer.powerconsumption["idle"]*ADCS_magnetorquer.number_included
            power_sunsensor=ADCS_sunsensor.powerconsumption["sampling"]*ADCS_sunsensor.number_included
            power_magnetometer=ADCS_magnetometer.powerconsumption["idle"]*ADCS_magnetometer.number_included
            power_IMU=ADCS_imu.powerconsumption["idle"]*ADCS_imu.number_included
            power_satnogs = COM_satnogs_board.powerconsumption["idle"]*COM_satnogs_board.number_included
            power_amateur=COM_amateur_radio.powerconsumption["idle"]*COM_amateur_radio.number_included
            power_pay=PAY_all.powerconsumption["idle"]*PAY_all.number_included
            
        case 6:
            power_reaction_wheels=ADCS_reactionweheels.powerconsumption["idle"]*ADCS_reactionweheels.number_included
            power_gnss=ADCS_GNSS_system.powerconsumption["idle"]*ADCS_GNSS_system.number_included
            power_magentorquer=ADCS_magnetorquer.powerconsumption["idle"]*ADCS_magnetorquer.number_included
            power_sunsensor=ADCS_sunsensor.powerconsumption["idle"]*ADCS_sunsensor.number_included
            power_magnetometer=ADCS_magnetometer.powerconsumption["ultra_high_res"]*ADCS_magnetometer.number_included
            power_IMU=ADCS_imu.powerconsumption["idle"]*ADCS_imu.number_included
            power_satnogs = COM_satnogs_board.powerconsumption["idle"]*COM_satnogs_board.number_included
            power_amateur=COM_amateur_radio.powerconsumption["idle"]*COM_amateur_radio.number_included
            power_pay=PAY_all.powerconsumption["idle"]*PAY_all.number_included
            
        case 7:
            power_reaction_wheels=ADCS_reactionweheels.powerconsumption["idle"]*ADCS_reactionweheels.number_included
            power_gnss=ADCS_GNSS_system.powerconsumption["idle"]*ADCS_GNSS_system.number_included
            power_magentorquer=ADCS_magnetorquer.powerconsumption["idle"]*ADCS_magnetorquer.number_included
            power_sunsensor=ADCS_sunsensor.powerconsumption["idle"]*ADCS_sunsensor.number_included
            power_magnetometer=ADCS_magnetometer.powerconsumption["idle"]*ADCS_magnetometer.number_included
            power_IMU=ADCS_imu.powerconsumption["gyroscope_accelerometer_high_per"]*ADCS_imu.number_included
            power_satnogs = COM_satnogs_board.powerconsumption["idle"]*COM_satnogs_board.number_included
            power_amateur=COM_amateur_radio.powerconsumption["idle"]*COM_amateur_radio.number_included
            power_pay=PAY_all.powerconsumption["idle"]*PAY_all.number_included
            
        case 8:
            power_reaction_wheels=ADCS_reactionweheels.powerconsumption["idle"]*ADCS_reactionweheels.number_included
            power_gnss=ADCS_GNSS_system.powerconsumption["idle"]*ADCS_GNSS_system.number_included
            power_magentorquer=ADCS_magnetorquer.powerconsumption["idle"]*ADCS_magnetorquer.number_included
            power_sunsensor=ADCS_sunsensor.powerconsumption["idle"]*ADCS_sunsensor.number_included
            power_magnetometer=ADCS_magnetometer.powerconsumption["idle"]*ADCS_magnetometer.number_included
            power_IMU=ADCS_imu.powerconsumption["idle"]*ADCS_imu.number_included
            power_satnogs = COM_satnogs_board.powerconsumption["transmit"]*COM_satnogs_board.number_included
            power_amateur=COM_amateur_radio.powerconsumption["idle"]*COM_amateur_radio.number_included
            power_pay=PAY_all.powerconsumption["idle"]*PAY_all.number_included
            
        case 9:
            power_reaction_wheels=ADCS_reactionweheels.powerconsumption["idle"]*ADCS_reactionweheels.number_included
            power_gnss=ADCS_GNSS_system.powerconsumption["idle"]*ADCS_GNSS_system.number_included
            power_magentorquer=ADCS_magnetorquer.powerconsumption["idle"]*ADCS_magnetorquer.number_included
            power_sunsensor=ADCS_sunsensor.powerconsumption["idle"]*ADCS_sunsensor.number_included
            power_magnetometer=ADCS_magnetometer.powerconsumption["idle"]*ADCS_magnetometer.number_included
            power_IMU=ADCS_imu.powerconsumption["idle"]*ADCS_imu.number_included
            power_satnogs = COM_satnogs_board.powerconsumption["idle"]*COM_satnogs_board.number_included
            power_amateur=COM_amateur_radio.powerconsumption["transmit"]*COM_amateur_radio.number_included
            power_pay=PAY_all.powerconsumption["idle"]*PAY_all.number_included
            
        case 10:
            power_reaction_wheels=ADCS_reactionweheels.powerconsumption["idle"]*ADCS_reactionweheels.number_included
            power_gnss=ADCS_GNSS_system.powerconsumption["idle"]*ADCS_GNSS_system.number_included
            power_magentorquer=ADCS_magnetorquer.powerconsumption["idle"]*ADCS_magnetorquer.number_included
            power_sunsensor=ADCS_sunsensor.powerconsumption["idle"]*ADCS_sunsensor.number_included
            power_magnetometer=ADCS_magnetometer.powerconsumption["idle"]*ADCS_magnetometer.number_included
            power_IMU=ADCS_imu.powerconsumption["idle"]*ADCS_imu.number_included
            power_satnogs = COM_satnogs_board.powerconsumption["idle"]*COM_satnogs_board.number_included
            power_amateur=COM_amateur_radio.powerconsumption["receive"]*COM_amateur_radio.number_included
            power_pay=PAY_all.powerconsumption["idle"]*PAY_all.number_included

        case 11:
            power_reaction_wheels=ADCS_reactionweheels.powerconsumption["idle"]*ADCS_reactionweheels.number_included
            power_gnss=ADCS_GNSS_system.powerconsumption["idle"]*ADCS_GNSS_system.number_included
            power_magentorquer=ADCS_magnetorquer.powerconsumption["idle"]*ADCS_magnetorquer.number_included
            power_sunsensor=ADCS_sunsensor.powerconsumption["idle"]*ADCS_sunsensor.number_included
            power_magnetometer=ADCS_magnetometer.powerconsumption["idle"]*ADCS_magnetometer.number_included
            power_IMU=ADCS_imu.powerconsumption["idle"]*ADCS_imu.number_included
            power_satnogs = COM_satnogs_board.powerconsumption["idle"]*COM_satnogs_board.number_included
            power_amateur=COM_amateur_radio.powerconsumption["Tx_relais"]*COM_amateur_radio.number_included
            power_pay=PAY_all.powerconsumption["idle"]*PAY_all.number_included

        case 12:
            power_reaction_wheels=ADCS_reactionweheels.powerconsumption["idle"]*ADCS_reactionweheels.number_included
            power_gnss=ADCS_GNSS_system.powerconsumption["idle"]*ADCS_GNSS_system.number_included
            power_magentorquer=ADCS_magnetorquer.powerconsumption["idle"]*ADCS_magnetorquer.number_included
            power_sunsensor=ADCS_sunsensor.powerconsumption["idle"]*ADCS_sunsensor.number_included
            power_magnetometer=ADCS_magnetometer.powerconsumption["idle"]*ADCS_magnetometer.number_included
            power_IMU=ADCS_imu.powerconsumption["idle"]*ADCS_imu.number_included
            power_satnogs = COM_satnogs_board.powerconsumption["idle"]*COM_satnogs_board.number_included
            power_amateur=COM_amateur_radio.powerconsumption["idle"]*COM_amateur_radio.number_included
            power_pay=PAY_all.powerconsumption["experiment"]*PAY_all.number_included
                
    #Default power consumption / Devices not to test
    power_eps=EPS_battery_board.powerconsumption["always"]*EPS_battery_board.number_included
    power_eps_solar=EPS_solarpanel.powerconsumption["idle"]*EPS_solarpanel.number_included
    power_obc=OBC_board.powerconsumption["always"]*OBC_board.number_included
    
    power_3_3=power_gnss+power_magentorquer+power_sunsensor+power_magnetometer+power_IMU+power_obc
    power_5=power_reaction_wheels+power_satnogs+power_amateur+power_eps_solar+power_pay
    power_from_bat=power_eps

    return power_3_3,power_5,power_from_bat

def Tx_initial_round(time):
    power_3_3=0
    power_5=0

    power_reaction_wheels=ADCS_reactionweheels.powerconsumption["idle"]*ADCS_reactionweheels.number_included
    power_gnss=ADCS_GNSS_system.powerconsumption["idle"]*ADCS_GNSS_system.number_included
    power_magentorquer=ADCS_magnetorquer.powerconsumption["idle"]*ADCS_magnetorquer.number_included
    power_sunsensor=ADCS_sunsensor.powerconsumption["idle"]*ADCS_sunsensor.number_included
    power_magnetometer=ADCS_magnetometer.powerconsumption["ultra_high_res"]*ADCS_magnetometer.number_included
    power_IMU=ADCS_imu.powerconsumption["idle"]*ADCS_imu.number_included
    power_satnogs = COM_satnogs_board.powerconsumption["transmit"]*COM_satnogs_board.number_included
    power_amateur=COM_amateur_radio.powerconsumption["idle"]*COM_amateur_radio.number_included
    power_eps=EPS_battery_board.powerconsumption["always"]*EPS_battery_board.number_included
    power_eps_solar=EPS_solarpanel.powerconsumption["idle"]*EPS_solarpanel.number_included
    power_obc=OBC_board.powerconsumption["always"]*OBC_board.number_included
    power_pay=PAY_all.powerconsumption["idle"]*PAY_all.number_included
    power_uhf=COM_uhf_antenna.powerconsumption["transmit"]*COM_uhf_antenna.number_included

    power_3_3=power_gnss+power_magentorquer+power_sunsensor+power_magnetometer+power_IMU+power_obc
    power_5=power_reaction_wheels+power_satnogs+power_amateur+power_eps_solar+power_pay+power_uhf
    power_from_bat=power_eps

    return power_3_3,power_5,power_from_bat

def Charge(time):
    power_3_3=0
    power_5=0

    power_reaction_wheels=ADCS_reactionweheels.powerconsumption["idle"]*ADCS_reactionweheels.number_included
    power_gnss=ADCS_GNSS_system.powerconsumption["idle"]*ADCS_GNSS_system.number_included
    power_magentorquer=ADCS_magnetorquer.powerconsumption["idle"]*ADCS_magnetorquer.number_included
    power_sunsensor=ADCS_sunsensor.powerconsumption["idle"]*ADCS_sunsensor.number_included
    power_magnetometer=ADCS_magnetometer.powerconsumption["ultra_high_res"]*ADCS_magnetometer.number_included
    power_IMU=ADCS_imu.powerconsumption["idle"]*ADCS_imu.number_included
    power_satnogs = COM_satnogs_board.powerconsumption["idle"]*COM_satnogs_board.number_included
    power_amateur=COM_amateur_radio.powerconsumption["idle"]*COM_amateur_radio.number_included
    power_eps=EPS_battery_board.powerconsumption["always"]*EPS_battery_board.number_included
    power_eps_solar=EPS_solarpanel.powerconsumption["idle"]*EPS_solarpanel.number_included
    power_obc=OBC_board.powerconsumption["always"]*OBC_board.number_included
    power_pay=PAY_all.powerconsumption["idle"]*PAY_all.number_included


    power_3_3=power_gnss+power_magentorquer+power_sunsensor+power_magnetometer+power_IMU+power_obc
    power_5=power_reaction_wheels+power_satnogs+power_amateur+power_eps_solar+power_pay
    power_from_bat=power_eps

    return power_3_3,power_5,power_from_bat

#Active for just 2 minutes
def Split(time):
    power_3_3=0
    power_5=0

    power_reaction_wheels=ADCS_reactionweheels.powerconsumption["idle"]*ADCS_reactionweheels.number_included
    power_gnss=ADCS_GNSS_system.powerconsumption["idle"]*ADCS_GNSS_system.number_included
    power_magentorquer=ADCS_magnetorquer.powerconsumption["idle"]*ADCS_magnetorquer.number_included
    power_sunsensor=ADCS_sunsensor.powerconsumption["idle"]*ADCS_sunsensor.number_included
    power_magnetometer=ADCS_magnetometer.powerconsumption["ultra_high_res"]*ADCS_magnetometer.number_included
    power_IMU=ADCS_imu.powerconsumption["idle"]*ADCS_imu.number_included
    power_satnogs = COM_satnogs_board.powerconsumption["idle"]*COM_satnogs_board.number_included
    power_amateur=COM_amateur_radio.powerconsumption["idle"]*COM_amateur_radio.number_included
    power_eps=EPS_battery_board.powerconsumption["always"]*EPS_battery_board.number_included
    power_eps_solar=EPS_solarpanel.powerconsumption["idle"]*EPS_solarpanel.number_included
    power_obc=OBC_board.powerconsumption["always"]*OBC_board.number_included
    power_pay=PAY_all.powerconsumption["experiment"]*PAY_all.number_included


    power_3_3=power_gnss+power_magentorquer+power_sunsensor+power_magnetometer+power_IMU+power_obc
    power_5=power_reaction_wheels+power_satnogs+power_amateur+power_eps_solar+power_pay
    power_from_bat=power_eps

    return power_3_3,power_5,power_from_bat

#5min
def Pointing(time):
    power_3_3=0
    power_5=0

    power_reaction_wheels=ADCS_reactionweheels.powerconsumption["average"]*ADCS_reactionweheels.number_included
    power_gnss=ADCS_GNSS_system.powerconsumption["idle"]*ADCS_GNSS_system.number_included
    power_magentorquer=ADCS_magnetorquer.powerconsumption["idle"]*ADCS_magnetorquer.number_included
    power_sunsensor=ADCS_sunsensor.powerconsumption["sampling"]*ADCS_sunsensor.number_included
    power_magnetometer=ADCS_magnetometer.powerconsumption["ultra_high_res"]*ADCS_magnetometer.number_included
    power_IMU=ADCS_imu.powerconsumption["idle"]*ADCS_imu.number_included
    power_satnogs = COM_satnogs_board.powerconsumption["idle"]*COM_satnogs_board.number_included
    power_amateur=COM_amateur_radio.powerconsumption["idle"]*COM_amateur_radio.number_included
    power_eps=EPS_battery_board.powerconsumption["always"]*EPS_battery_board.number_included
    power_eps_solar=EPS_solarpanel.powerconsumption["idle"]*EPS_solarpanel.number_included
    power_obc=OBC_board.powerconsumption["always"]*OBC_board.number_included
    power_pay=PAY_all.powerconsumption["idle"]*PAY_all.number_included


    power_3_3=power_gnss+power_magentorquer+power_sunsensor+power_magnetometer+power_IMU+power_obc
    power_5=power_reaction_wheels+power_satnogs+power_amateur+power_eps_solar+power_pay
    power_from_bat=power_eps

    return power_3_3,power_5,power_from_bat

def Desaturation(time):
    power_3_3=0
    power_5=0

    power_reaction_wheels=ADCS_reactionweheels.powerconsumption["max_torque"]*ADCS_reactionweheels.number_included
    power_gnss=ADCS_GNSS_system.powerconsumption["idle"]*ADCS_GNSS_system.number_included
    power_magentorquer=ADCS_magnetorquer.powerconsumption["peak"]*ADCS_magnetorquer.number_included
    power_sunsensor=ADCS_sunsensor.powerconsumption["idle"]*ADCS_sunsensor.number_included
    power_magnetometer=ADCS_magnetometer.powerconsumption["ultra_high_res"]*ADCS_magnetometer.number_included
    power_IMU=ADCS_imu.powerconsumption["idle"]*ADCS_imu.number_included
    power_satnogs = COM_satnogs_board.powerconsumption["idle"]*COM_satnogs_board.number_included
    power_amateur=COM_amateur_radio.powerconsumption["idle"]*COM_amateur_radio.number_included
    power_eps=EPS_battery_board.powerconsumption["always"]*EPS_battery_board.number_included
    power_eps_solar=EPS_solarpanel.powerconsumption["idle"]*EPS_solarpanel.number_included
    power_obc=OBC_board.powerconsumption["always"]*OBC_board.number_included
    power_pay=PAY_all.powerconsumption["idle"]*PAY_all.number_included


    power_3_3=power_gnss+power_magentorquer+power_sunsensor+power_magnetometer+power_IMU+power_obc
    power_5=power_reaction_wheels+power_satnogs+power_amateur+power_eps_solar+power_pay
    power_from_bat=power_eps

    return power_3_3,power_5,power_from_bat

def TX_regular(time):
    power_3_3=0
    power_5=0

    power_reaction_wheels=ADCS_reactionweheels.powerconsumption["average"]*ADCS_reactionweheels.number_included
    power_gnss=ADCS_GNSS_system.powerconsumption["idle"]*ADCS_GNSS_system.number_included
    power_magentorquer=ADCS_magnetorquer.powerconsumption["idle"]*ADCS_magnetorquer.number_included
    power_sunsensor=ADCS_sunsensor.powerconsumption["idle"]*ADCS_sunsensor.number_included
    power_magnetometer=ADCS_magnetometer.powerconsumption["ultra_high_res"]*ADCS_magnetometer.number_included
    power_IMU=ADCS_imu.powerconsumption["idle"]*ADCS_imu.number_included
    power_satnogs = COM_satnogs_board.powerconsumption["transmit"]*COM_satnogs_board.number_included
    power_amateur=COM_amateur_radio.powerconsumption["idle"]*COM_amateur_radio.number_included
    power_eps=EPS_battery_board.powerconsumption["always"]*EPS_battery_board.number_included
    power_eps_solar=EPS_solarpanel.powerconsumption["idle"]*EPS_solarpanel.number_included
    power_obc=OBC_board.powerconsumption["always"]*OBC_board.number_included
    power_pay=PAY_all.powerconsumption["idle"]*PAY_all.number_included
    power_uhf=COM_uhf_antenna.powerconsumption["transmit"]*COM_uhf_antenna.number_included

    power_3_3=power_gnss+power_magentorquer+power_sunsensor+power_magnetometer+power_IMU+power_obc
    power_5=power_reaction_wheels+power_satnogs+power_amateur+power_eps_solar+power_pay+power_uhf
    power_from_bat=power_eps

    return power_3_3,power_5,power_from_bat

def RX_regular(time):
    power_3_3=0
    power_5=0

    power_reaction_wheels=ADCS_reactionweheels.powerconsumption["average"]*ADCS_reactionweheels.number_included
    power_gnss=ADCS_GNSS_system.powerconsumption["idle"]*ADCS_GNSS_system.number_included
    power_magentorquer=ADCS_magnetorquer.powerconsumption["idle"]*ADCS_magnetorquer.number_included
    power_sunsensor=ADCS_sunsensor.powerconsumption["idle"]*ADCS_sunsensor.number_included
    power_magnetometer=ADCS_magnetometer.powerconsumption["ultra_high_res"]*ADCS_magnetometer.number_included
    power_IMU=ADCS_imu.powerconsumption["idle"]*ADCS_imu.number_included
    power_satnogs = COM_satnogs_board.powerconsumption["receive"]*COM_satnogs_board.number_included
    power_amateur=COM_amateur_radio.powerconsumption["idle"]*COM_amateur_radio.number_included
    power_eps=EPS_battery_board.powerconsumption["always"]*EPS_battery_board.number_included
    power_eps_solar=EPS_solarpanel.powerconsumption["idle"]*EPS_solarpanel.number_included
    power_obc=OBC_board.powerconsumption["always"]*OBC_board.number_included
    power_pay=PAY_all.powerconsumption["idle"]*PAY_all.number_included
    power_uhf=COM_uhf_antenna.powerconsumption["transmit"]*COM_uhf_antenna.number_included

    power_3_3=power_gnss+power_magentorquer+power_sunsensor+power_magnetometer+power_IMU+power_obc
    power_5=power_reaction_wheels+power_satnogs+power_amateur+power_eps_solar+power_pay+power_uhf
    power_from_bat=power_eps

    return power_3_3,power_5,power_from_bat

def Spin_Up(time):
    power_3_3=0
    power_5=0

    power_reaction_wheels=ADCS_reactionweheels.powerconsumption["max_torque"]*ADCS_reactionweheels.number_included
    power_gnss=ADCS_GNSS_system.powerconsumption["idle"]*ADCS_GNSS_system.number_included
    power_magentorquer=ADCS_magnetorquer.powerconsumption["peak"]*ADCS_magnetorquer.number_included
    power_sunsensor=ADCS_sunsensor.powerconsumption["idle"]*ADCS_sunsensor.number_included
    power_magnetometer=ADCS_magnetometer.powerconsumption["ultra_high_res"]*ADCS_magnetometer.number_included
    power_IMU=ADCS_imu.powerconsumption["idle"]*ADCS_imu.number_included
    power_satnogs = COM_satnogs_board.powerconsumption["idle"]*COM_satnogs_board.number_included
    power_amateur=COM_amateur_radio.powerconsumption["idle"]*COM_amateur_radio.number_included
    power_eps=EPS_battery_board.powerconsumption["always"]*EPS_battery_board.number_included
    power_eps_solar=EPS_solarpanel.powerconsumption["idle"]*EPS_solarpanel.number_included
    power_obc=OBC_board.powerconsumption["always"]*OBC_board.number_included
    power_pay=PAY_all.powerconsumption["idle"]*PAY_all.number_included
    power_uhf=COM_uhf_antenna.powerconsumption["idle"]*COM_uhf_antenna.number_included

    power_3_3=power_gnss+power_magentorquer+power_sunsensor+power_magnetometer+power_IMU+power_obc
    power_5=power_reaction_wheels+power_satnogs+power_amateur+power_eps_solar+power_pay+power_uhf
    power_from_bat=power_eps

    return power_3_3,power_5,power_from_bat

def Spin_Down(time):
    power_3_3=0
    power_5=0

    power_reaction_wheels=ADCS_reactionweheels.powerconsumption["max_torque"]*ADCS_reactionweheels.number_included
    power_gnss=ADCS_GNSS_system.powerconsumption["idle"]*ADCS_GNSS_system.number_included
    power_magentorquer=ADCS_magnetorquer.powerconsumption["peak"]*ADCS_magnetorquer.number_included
    power_sunsensor=ADCS_sunsensor.powerconsumption["idle"]*ADCS_sunsensor.number_included
    power_magnetometer=ADCS_magnetometer.powerconsumption["ultra_high_res"]*ADCS_magnetometer.number_included
    power_IMU=ADCS_imu.powerconsumption["idle"]*ADCS_imu.number_included
    power_satnogs = COM_satnogs_board.powerconsumption["idle"]*COM_satnogs_board.number_included
    power_amateur=COM_amateur_radio.powerconsumption["idle"]*COM_amateur_radio.number_included
    power_eps=EPS_battery_board.powerconsumption["always"]*EPS_battery_board.number_included
    power_eps_solar=EPS_solarpanel.powerconsumption["idle"]*EPS_solarpanel.number_included
    power_obc=OBC_board.powerconsumption["always"]*OBC_board.number_included
    power_pay=PAY_all.powerconsumption["idle"]*PAY_all.number_included
    power_uhf=COM_uhf_antenna.powerconsumption["idle"]*COM_uhf_antenna.number_included

    power_3_3=power_gnss+power_magentorquer+power_sunsensor+power_magnetometer+power_IMU+power_obc
    power_5=power_reaction_wheels+power_satnogs+power_amateur+power_eps_solar+power_pay+power_uhf
    power_from_bat=power_eps

    return power_3_3,power_5,power_from_bat

def Experiment(time):
    power_3_3=0
    power_5=0

    power_reaction_wheels=ADCS_reactionweheels.powerconsumption["average"]*ADCS_reactionweheels.number_included
    power_gnss=ADCS_GNSS_system.powerconsumption["idle"]*ADCS_GNSS_system.number_included
    power_magentorquer=ADCS_magnetorquer.powerconsumption["idle"]*ADCS_magnetorquer.number_included
    power_sunsensor=ADCS_sunsensor.powerconsumption["idle"]*ADCS_sunsensor.number_included
    power_magnetometer=ADCS_magnetometer.powerconsumption["ultra_high_res"]*ADCS_magnetometer.number_included
    power_IMU=ADCS_imu.powerconsumption["idle"]*ADCS_imu.number_included
    power_satnogs = COM_satnogs_board.powerconsumption["idle"]*COM_satnogs_board.number_included
    power_amateur=COM_amateur_radio.powerconsumption["idle"]*COM_amateur_radio.number_included
    power_eps=EPS_battery_board.powerconsumption["always"]*EPS_battery_board.number_included
    power_eps_solar=EPS_solarpanel.powerconsumption["idle"]*EPS_solarpanel.number_included
    power_obc=OBC_board.powerconsumption["always"]*OBC_board.number_included
    power_pay=PAY_all.powerconsumption["idle"]*PAY_all.number_included
    power_uhf=COM_uhf_antenna.powerconsumption["idle"]*COM_uhf_antenna.number_included

    power_3_3=power_gnss+power_magentorquer+power_sunsensor+power_magnetometer+power_IMU+power_obc
    power_5=power_reaction_wheels+power_satnogs+power_amateur+power_eps_solar+power_pay+power_uhf
    power_from_bat=power_eps

    return power_3_3,power_5,power_from_bat

def GNSS_positioning_scientific(time):
    power_3_3=0
    power_5=0

    power_reaction_wheels=ADCS_reactionweheels.powerconsumption["average"]*ADCS_reactionweheels.number_included
    power_gnss=ADCS_GNSS_system.powerconsumption["scientific_mode"]*ADCS_GNSS_system.number_included
    power_magentorquer=ADCS_magnetorquer.powerconsumption["idle"]*ADCS_magnetorquer.number_included
    power_sunsensor=ADCS_sunsensor.powerconsumption["idle"]*ADCS_sunsensor.number_included
    power_magnetometer=ADCS_magnetometer.powerconsumption["ultra_high_res"]*ADCS_magnetometer.number_included
    power_IMU=ADCS_imu.powerconsumption["idle"]*ADCS_imu.number_included
    power_satnogs = COM_satnogs_board.powerconsumption["idle"]*COM_satnogs_board.number_included
    power_amateur=COM_amateur_radio.powerconsumption["idle"]*COM_amateur_radio.number_included
    power_eps=EPS_battery_board.powerconsumption["always"]*EPS_battery_board.number_included
    power_eps_solar=EPS_solarpanel.powerconsumption["idle"]*EPS_solarpanel.number_included
    power_obc=OBC_board.powerconsumption["always"]*OBC_board.number_included
    power_pay=PAY_all.powerconsumption["idle"]*PAY_all.number_included
    power_uhf=COM_uhf_antenna.powerconsumption["idle"]*COM_uhf_antenna.number_included

    power_3_3=power_gnss+power_magentorquer+power_sunsensor+power_magnetometer+power_IMU+power_obc
    power_5=power_reaction_wheels+power_satnogs+power_amateur+power_eps_solar+power_pay+power_uhf
    power_from_bat=power_eps

    return power_3_3,power_5,power_from_bat

def GNSS_positioning_pvt(time):
    power_3_3=0
    power_5=0

    power_reaction_wheels=ADCS_reactionweheels.powerconsumption["average"]*ADCS_reactionweheels.number_included
    power_gnss=ADCS_GNSS_system.powerconsumption["PVT_mode"]*ADCS_GNSS_system.number_included
    power_magentorquer=ADCS_magnetorquer.powerconsumption["idle"]*ADCS_magnetorquer.number_included
    power_sunsensor=ADCS_sunsensor.powerconsumption["idle"]*ADCS_sunsensor.number_included
    power_magnetometer=ADCS_magnetometer.powerconsumption["ultra_high_res"]*ADCS_magnetometer.number_included
    power_IMU=ADCS_imu.powerconsumption["idle"]*ADCS_imu.number_included
    power_satnogs = COM_satnogs_board.powerconsumption["idle"]*COM_satnogs_board.number_included
    power_amateur=COM_amateur_radio.powerconsumption["idle"]*COM_amateur_radio.number_included
    power_eps=EPS_battery_board.powerconsumption["always"]*EPS_battery_board.number_included
    power_eps_solar=EPS_solarpanel.powerconsumption["idle"]*EPS_solarpanel.number_included
    power_obc=OBC_board.powerconsumption["always"]*OBC_board.number_included
    power_pay=PAY_all.powerconsumption["idle"]*PAY_all.number_included
    power_uhf=COM_uhf_antenna.powerconsumption["idle"]*COM_uhf_antenna.number_included

    power_3_3=power_gnss+power_magentorquer+power_sunsensor+power_magnetometer+power_IMU+power_obc
    power_5=power_reaction_wheels+power_satnogs+power_amateur+power_eps_solar+power_pay+power_uhf
    power_from_bat=power_eps

    return power_3_3,power_5,power_from_bat

def Beacon(time):
    power_3_3=0
    power_5=0

    power_reaction_wheels=ADCS_reactionweheels.powerconsumption["idle"]*ADCS_reactionweheels.number_included
    power_gnss=ADCS_GNSS_system.powerconsumption["idle"]*ADCS_GNSS_system.number_included
    power_magentorquer=ADCS_magnetorquer.powerconsumption["idle"]*ADCS_magnetorquer.number_included
    power_sunsensor=ADCS_sunsensor.powerconsumption["idle"]*ADCS_sunsensor.number_included
    power_magnetometer=ADCS_magnetometer.powerconsumption["low_power"]*ADCS_magnetometer.number_included
    power_IMU=ADCS_imu.powerconsumption["idle"]*ADCS_imu.number_included
    power_satnogs = COM_satnogs_board.powerconsumption["transmit"]*COM_satnogs_board.number_included
    power_amateur=COM_amateur_radio.powerconsumption["idle"]*COM_amateur_radio.number_included
    power_eps=EPS_battery_board.powerconsumption["always"]*EPS_battery_board.number_included
    power_eps_solar=EPS_solarpanel.powerconsumption["idle"]*EPS_solarpanel.number_included
    power_obc=OBC_board.powerconsumption["always"]*OBC_board.number_included
    power_pay=PAY_all.powerconsumption["idle"]*PAY_all.number_included
    power_uhf=COM_uhf_antenna.powerconsumption["idle"]*COM_uhf_antenna.number_included

    power_3_3=power_gnss+power_magentorquer+power_sunsensor+power_magnetometer+power_IMU+power_obc
    power_5=power_reaction_wheels+power_satnogs+power_amateur+power_eps_solar+power_pay+power_uhf
    power_from_bat=power_eps

    return power_3_3,power_5,power_from_bat

def Critical(time):
    power_3_3=0
    power_5=0

    power_reaction_wheels=ADCS_reactionweheels.powerconsumption["idle"]*ADCS_reactionweheels.number_included
    power_gnss=ADCS_GNSS_system.powerconsumption["off"]*ADCS_GNSS_system.number_included
    power_magentorquer=ADCS_magnetorquer.powerconsumption["idle"]*ADCS_magnetorquer.number_included
    power_sunsensor=ADCS_sunsensor.powerconsumption["idle"]*ADCS_sunsensor.number_included
    power_magnetometer=ADCS_magnetometer.powerconsumption["low_power"]*ADCS_magnetometer.number_included
    power_IMU=ADCS_imu.powerconsumption["idle"]*ADCS_imu.number_included
    power_satnogs = COM_satnogs_board.powerconsumption["idle"]*COM_satnogs_board.number_included
    power_amateur=COM_amateur_radio.powerconsumption["idle"]*COM_amateur_radio.number_included
    power_eps=EPS_battery_board.powerconsumption["always"]*EPS_battery_board.number_included
    power_eps_solar=EPS_solarpanel.powerconsumption["idle"]*EPS_solarpanel.number_included
    power_obc=OBC_board.powerconsumption["always"]*OBC_board.number_included
    power_pay=PAY_all.powerconsumption["emergency"]*PAY_all.number_included
    power_uhf=COM_uhf_antenna.powerconsumption["idle"]*COM_uhf_antenna.number_included

    power_3_3=power_gnss+power_magentorquer+power_sunsensor+power_magnetometer+power_IMU+power_obc
    power_5=power_reaction_wheels+power_satnogs+power_amateur+power_eps_solar+power_pay+power_uhf
    power_from_bat=power_eps

    return power_3_3,power_5,power_from_bat

def Emergency(time):
    power_3_3=0
    power_5=0

    power_reaction_wheels=ADCS_reactionweheels.powerconsumption["idle"]*ADCS_reactionweheels.number_included
    power_gnss=ADCS_GNSS_system.powerconsumption["off"]*ADCS_GNSS_system.number_included
    power_magentorquer=ADCS_magnetorquer.powerconsumption["idle"]*ADCS_magnetorquer.number_included
    power_sunsensor=ADCS_sunsensor.powerconsumption["idle"]*ADCS_sunsensor.number_included
    power_magnetometer=ADCS_magnetometer.powerconsumption["low_power"]*ADCS_magnetometer.number_included
    power_IMU=ADCS_imu.powerconsumption["idle"]*ADCS_imu.number_included
    power_satnogs = COM_satnogs_board.powerconsumption["idle"]*COM_satnogs_board.number_included
    power_amateur=COM_amateur_radio.powerconsumption["idle"]*COM_amateur_radio.number_included
    power_eps=EPS_battery_board.powerconsumption["always"]*EPS_battery_board.number_included
    power_eps_solar=EPS_solarpanel.powerconsumption["idle"]*EPS_solarpanel.number_included
    power_obc=OBC_board.powerconsumption["always"]*OBC_board.number_included
    power_pay=PAY_all.powerconsumption["off"]*PAY_all.number_included
    power_uhf=COM_uhf_antenna.powerconsumption["idle"]*COM_uhf_antenna.number_included

    power_3_3=power_gnss+power_magentorquer+power_sunsensor+power_magnetometer+power_IMU+power_obc
    power_5=power_reaction_wheels+power_satnogs+power_amateur+power_eps_solar+power_pay+power_uhf
    power_from_bat=power_eps

    return power_3_3,power_5,power_from_bat
