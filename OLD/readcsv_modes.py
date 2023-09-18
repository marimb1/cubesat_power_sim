import csv

power_magnetorquer=[]
duration_magnetorquer=[]
power_reactionwheels=[]
duartion_reactionwheels=[]
power_gps=[]
duration_gps=[]
power_imu=[]
duration_imu=[]
power_magnetometer=[]
duration_magnetometer=[]
power_sunsensor=[]
duration_sunsensor=[]
power_satnogs=[]
duration_satnogs=[]
power_satnogssband=[]
duration_satnogssband=[]
power_uhfdeploy=[]
duration_uhfdeploy=[]
power_amteurradio=[]
duration_amateurradio=[]
power_powermodule=[]
duration_powermodule=[]
power_solarpanel=[]
duration_solarpanel=[]
power_mainboard=[]
duration_mainboard=[]
power_payload=[]
duration_payload=[]

def readfile():
    with open('Powerbudgetscsv.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        i=0
        for row in reader:
            if i>0:
                power_magnetorquer.append(row[1])
                duration_magnetorquer.append(row[2])
                power_reactionwheels.append(row[3])
                duartion_reactionwheels.append(row[4])
                power_gps.append(row[5])
                duration_gps.append(row[6])
                power_imu.append(row[7])
                duration_imu.append(row[8])
                power_magnetometer.append(row[9])
                duration_magnetometer.append(row[10])
                power_sunsensor.append(row[11])
                duration_sunsensor.append(row[12])
                power_satnogs.append(row[13])
                duration_satnogs.append(row[14])
                power_satnogssband.append(row[15])
                duration_satnogssband.append(row[16])
                power_uhfdeploy.append(row[17])
                duration_uhfdeploy.append(row[18])
                power_amteurradio.append(row[19])
                duration_amateurradio.append(row[20])
                power_powermodule.append(row[21])
                duration_powermodule.append(row[22])
                power_solarpanel.append(row[23])
                duration_solarpanel.append(row[24])
                power_mainboard.append(row[25])
                duration_mainboard.append(row[26])
                power_payload.append(row[27])
                duration_payload.append(row[28])
            i=i+1
                
    print("Power GPS: ")
    print(power_gps)
    print(duration_gps)

    print("Power IMU: ")
    print(power_imu)
    print(duration_imu)

    print("Power Magnetometer: ")
    print(power_magnetometer)
    print(duration_magnetometer)

    print("Power SunSensor: ")
    print(power_sunsensor)
    print(duration_sunsensor)

    print("Power SatNogsUHF: ")
    print(power_satnogs)
    print(duration_satnogs)

    print("Power SatNogsSband: ")
    print(power_satnogssband)
    print(duration_satnogssband)

    print("Power UHF deploy: ")
    print(power_uhfdeploy)
    print(duration_uhfdeploy)

    print("Power amateur radio: ")
    print(power_amteurradio)
    print(duration_amateurradio)

    print("Power power moudle: ")
    print(power_powermodule)
    print(duration_powermodule)

    print("Power Solarpanels: ")
    print(power_solarpanel)
    print(duration_solarpanel)

    print("Power Mainboard: ")
    print(power_mainboard)
    print(duration_mainboard)

    print("Power Payload: ")
    print(power_payload)
    print(duration_payload)

readfile()