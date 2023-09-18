


class system:
    def __init__(self,modes,anzahl):
        self.powerconsumption=modes
        self.number_included=anzahl

#Efficiency of Buck_boost:(Datasheet from P31U)
def get_efficiency(voltage,current):
    if voltage==3.3:
        eff=-0.03*current+0.93
    elif voltage==5:
        eff=-0.02916+0.94
    else:
        eff=0
    return eff
    
#GNSS components:
#based on components in 05 Systems engineering 01 components 01System

#Watt at 3.3V
ADCS_GNSS_system = system({"off":0,
                        "idle":0.0165,
                         "PVT_mode":0.5841,
                         "scientific_mode":1.0824},1)
#Watt at 5V for 1 raction wheels
#https://gomspace.com/UserFiles/Subsystems/datasheet/gs-ds-nanotorque-gsw-600-20.pdf
#https://arisswitzerland.sharepoint.com/03_Projects/Forms/AllItems.aspx?id=%2F03%5FProjects%2F2022%5FSAGE%5FCubeSat%20Mission%2F05%5FSystems%20Engineering%2FAll%20Component%20Datasheets%2F01%5FADCS%2FReactionWheels%2FCubeWheel%2DBrochure%2DAugust%2D2016%2Epdf&viewid=134083a6%2D333a%2D4349%2Dba82%2De94bf146e8d3&parent=%2F03%5FProjects%2F2022%5FSAGE%5FCubeSat%20Mission%2F05%5FSystems%20Engineering%2FAll%20Component%20Datasheets%2F01%5FADCS%2FReactionWheels
ADCS_reactionweheels = system({"idle":0,
                               "max_torque":2.5,
                               "average":0.3},3)

#https://gomspace.com/shop/subsystems/attitude-orbit-control-systems/nanotorque-gst-600.aspx
#https://ssdl.gatech.edu/sites/default/files/ssdl-files/papers/mastersProjects/TadankiA-8900.pdf
#Watt at 3.3V
ADCS_magnetorquer = system({"idle":0.175,
                            "peak":1.2},1)

#https://gomspace.com/UserFiles/Subsystems/datasheet/gs-ds-nanosense-fss-31.pdf
#W at 3.3V
ADCS_sunsensor=system({"idle":0.0000264,
                       "sampling":0.01155},1)

#coarse sun sensor missing

#W at 3.3V
#https://arisswitzerland.sharepoint.com/03_Projects/Forms/AllItems.aspx?id=%2F03%5FProjects%2F2022%5FSAGE%5FCubeSat%20Mission%2F22%5FOBC%20%26%20ADCS%2F20%5FComponents%2F03%5FOBC%5FPCB%2F04%5FSensors%2F02%5FMagnetometer%2F01%5Flis3mdl%5Fdatasheet%2Epdf&viewid=134083a6%2D333a%2D4349%2Dba82%2De94bf146e8d3&parent=%2F03%5FProjects%2F2022%5FSAGE%5FCubeSat%20Mission%2F22%5FOBC%20%26%20ADCS%2F20%5FComponents%2F03%5FOBC%5FPCB%2F04%5FSensors%2F02%5FMagnetometer
ADCS_magnetometer = system({"idle":0,
                            "ultra_high_res":0.033,
                            "low_power":0.00165},4)

#https://arisswitzerland.sharepoint.com/03_Projects/Forms/AllItems.aspx?id=%2F03%5FProjects%2F2022%5FSAGE%5FCubeSat%20Mission%2F22%5FOBC%20%26%20ADCS%2F20%5FComponents%2F03%5FOBC%5FPCB%2F04%5FSensors%2F01%5FIMU%2F01%5Fism330dlc%5Fdatasheet%2Epdf&viewid=134083a6%2D333a%2D4349%2Dba82%2De94bf146e8d3&parent=%2F03%5FProjects%2F2022%5FSAGE%5FCubeSat%20Mission%2F22%5FOBC%20%26%20ADCS%2F20%5FComponents%2F03%5FOBC%5FPCB%2F04%5FSensors%2F01%5FIMU
#W at 3.3V (system would be better in 1.8V)
ADCS_imu = system({"idle":0.0000099,
                   "gyroscope_accelerometer_high_per":0.002475,
                   "gyroscope_accelerometer_normal":0.00165,
                   "gyroscope_accelerometer_low_power":0.001155,
                   "accelerometer_high_per":0.000627,
                   "acceleronter_normal":0.0002805,
                   "accelerometer_low_power":0.0000297},4)
#W at 8V
#https://arisswitzerland.sharepoint.com/03_Projects/Forms/AllItems.aspx?id=%2F03%5FProjects%2F2022%5FSAGE%5FCubeSat%20Mission%2F20%5FCOM%2F10%20SatNogs%20Comms%2FSatNOGS%2DCOMMS%2Dproduct%2Dsheet%2D2%2Epdf&parent=%2F03%5FProjects%2F2022%5FSAGE%5FCubeSat%20Mission%2F20%5FCOM%2F10%20SatNogs%20Comms
COM_satnogs_board = system({"idle":0,
                            "deploy":15,
                            "transmit":8,
                            "receive":5},1)

#https://arisswitzerland.sharepoint.com/03_Projects/Forms/AllItems.aspx?id=%2F03%5FProjects%2F2022%5FSAGE%5FCubeSat%20Mission%2F20%5FCOM%2F11%20UHF%20Antenna%2Fgs%2Dds%2Dnanocom%2Dant430%2D41%2Epdf&viewid=134083a6%2D333a%2D4349%2Dba82%2De94bf146e8d3&parent=%2F03%5FProjects%2F2022%5FSAGE%5FCubeSat%20Mission%2F20%5FCOM%2F11%20UHF%20Antenna
#W at 5V
COM_uhf_antenna = system({"idle":0,
                            "transmit":10},1)


#https://arisswitzerland.sharepoint.com/03_Projects/Forms/AllItems.aspx?id=%2F03%5FProjects%2F2022%5FSAGE%5FCubeSat%20Mission%2F20%5FCOM%2F09%20Amateur%20Payload%2FAmateur%20Radio%20Meetings%2FAMSAT%2DHB%20%2D%20SAGE%20Transponder%20Telco%2025%2DNOV%2D2021%20HB9ARK%2Epdf&viewid=134083a6%2D333a%2D4349%2Dba82%2De94bf146e8d3&parent=%2F03%5FProjects%2F2022%5FSAGE%5FCubeSat%20Mission%2F20%5FCOM%2F09%20Amateur%20Payload%2FAmateur%20Radio%20Meetings
COM_amateur_radio = system({"idle":0,
                            "transmit":3.396,
                            "receive":1.217,
                            "Tx_relais":4.437,},1)
#W directly from battery
#for heater W for 8V
#https://arisswitzerland.sharepoint.com/03_Projects/Forms/AllItems.aspx?id=%2F03%5FProjects%2F2022%5FSAGE%5FCubeSat%20Mission%2F21%5FEPS%2F04%20EPS%20Subsystem%20Files%2FEPS%20Board%20P31U%2Fdatasheet%2Dnanopower%2Dp31u%2Epdf&viewid=134083a6%2D333a%2D4349%2Dba82%2De94bf146e8d3&parent=%2F03%5FProjects%2F2022%5FSAGE%5FCubeSat%20Mission%2F21%5FEPS%2F04%20EPS%20Subsystem%20Files%2FEPS%20Board%20P31U
EPS_battery_board = system({"always":0.26,
                            "heater":3,
                            "battery_heater":6},1)
#efficiency for PV converters at different Power in. See datasheet from P31U
EPS_PV_converter=system({"0":0.94,
                         "1":0.94,
                         "2":0.95,
                         "3":0.96,
                         "4":0.97,
                         "5":0.965,
                         "6":0.965,
                         "7":0.96,
                         "8":0.95,
                         "9":0.95,
                         "10":0.95,
                         "11":0.95},3)

#W at 5V
#https://arisswitzerland.sharepoint.com/03_Projects/Forms/AllItems.aspx?id=%2F03%5FProjects%2F2022%5FSAGE%5FCubeSat%20Mission%2F21%5FEPS%2F04%20EPS%20Subsystem%20Files%2FSolar%20Panels%2FDatasheets%2FES%5F3U%5FSolar%5FPanel%5FDatasheet%2Epdf&viewid=134083a6%2D333a%2D4349%2Dba82%2De94bf146e8d3&parent=%2F03%5FProjects%2F2022%5FSAGE%5FCubeSat%20Mission%2F21%5FEPS%2F04%20EPS%20Subsystem%20Files%2FSolar%20Panels%2FDatasheets
EPS_solarpanel = system({"idle":0.055},3)

#W at 3.3V nothin available until now
OBC_board = system({"always":1},1)

#In Watt, nothing available!
PAY_all = system({"off":0,
                  "idle":3,
                  "emergency":1,
                  "experiment":8},1)