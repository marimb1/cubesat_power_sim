from variables import *
from subcomponents import *
import math

#Calculate No Sun angle (sat behind earth)
powerproduction_factor_panel1=[]             #factor is 1 if one solarpanel is pointing exactly to the sun.
powerproduction_factor_panel2=[] 
powerproduction_factor_panel3=[] 
px1b=[]
py1b=[]
pz1b=[]
anglex1test=[]
anglehtest=[]
def powerproduction_orbit(satellite,idx):
    dist=math.sqrt(float(orbit_x_sat[idx])**2+float(orbit_y_sat[idx])**2+float(orbit_z_sat[idx])**2)
    

    sat_sun_x=satellite.orbit_x[-1]
    sat_sun_y=satellite.orbit_y[-1]
    sat_sun_z=satellite.orbit_z[-1]

    #Panel 1
    angle_xy=math.tan(sat_sun_x/sat_sun_y)
    angle_h=math.cos((math.sqrt(float(orbit_x_sat[idx])**2+float(orbit_y_sat[idx])**2))/dist)
    

    px1=math.cos((satellite.angle_y[-1]-angle_h)/180*math.pi)*math.cos((satellite.angle_z[-1]-angle_xy)/180*math.pi)
    if px1>0:
        px1b.append(px1)
        powerproduction_factor_panel1.append(px1)
    else:
        px1b.append(0)
        powerproduction_factor_panel1.append(0)

    #Panel 2
    px2=math.cos((satellite.angle_x[-1]-angle_h)/180*math.pi)*math.cos((satellite.angle_z[-1]-angle_xy+90)/180*math.pi)

    if px2>0:
        py1b.append(px2)
        powerproduction_factor_panel2.append(px2)
    else:
        py1b.append(0)
        powerproduction_factor_panel2.append(0)
    anglex1test.append(satellite.angle_z[-1])
    anglehtest.append(angle_xy-90+45)

    #Panel 3
    px3=math.cos((satellite.angle_x[-1]-angle_h)/180*math.pi)*math.cos((satellite.angle_z[-1]-angle_xy+270)/180*math.pi)
   
    if px3>0:
        pz1b.append(px3)
        powerproduction_factor_panel3.append(px3)
    else:
        pz1b.append(0)
        powerproduction_factor_panel3.append(0)



def solarpanel_degredation(t,panel1=0,panel2=0,panel3=0):
    degredationfactor=(0.98)**(time_step/(365*24*60*60))
    #Degredation for panels including additional degredation
    deg1=health_panel1[-1]*degredationfactor*(1-panel1)
    deg2=health_panel2[-1]*degredationfactor*(1-panel2)
    deg3=health_panel3[-1]*degredationfactor*(1-panel3)
    health_panel1.append(deg1)
    health_panel2.append(deg2)
    health_panel3.append(deg3)
def powerfrompanel(idx):
    P1=powerproduction_factor_panel1[-1]*health_panel1[-1]*solarpanel_1_power*0.98
    arg=str(round(P1))
    P1_eff=P1*EPS_PV_converter.powerconsumption[arg]
    P2=powerproduction_factor_panel2[-1]*health_panel2[-1]*solarpanel_2_power*0.98
    arg2=str(round(P2))
    P2_eff=P2*EPS_PV_converter.powerconsumption[arg2]
    P3=powerproduction_factor_panel3[-1]*health_panel3[-1]*solarpanel_3_power*0.98
    arg3=str(round(P3))
    P3_eff=P3*EPS_PV_converter.powerconsumption[arg3]

    
    
    #Look if satellite is behind earth
    if orbit_sat_in_sun[idx]=='False':
        panel1_power.append(0)
        panel2_power.append(0)
        panel3_power.append(0)
        panel_all_power.append(0)
        return 0
    else:
        panel1_power.append(P1_eff)
        panel2_power.append(P2_eff)
        panel3_power.append(P3_eff)
        panel_all_power.append(P1+P2+P3)
        return P1_eff+P2_eff+P3_eff
    