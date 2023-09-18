from variables import *
import math

class cubesat:
    def __init__(self):
        self.age=[0]
        #self.angle_to_sun=[]
        self.angle_x=[angle_1]
        self.angle_y=[angle_2]
        self.angle_z=[angle_3]
        self.orbit_x=[]
        self.orbit_y=[]
        self.orbit_z=[]
        self.rotational_speed_x=[rotational_speed_x]
        self.rotational_speed_y=[rotational_speed_y]
        self.rotational_speed_z=[rotational_speed_z]
        #self.distance_to_sun=[distance]
        # self.temperature=[temperature]
        # self.power_mode=[initial_powermode]

        #Add one time step to cubesat
    def add_values(self,age,angle1,angle2,angle3,distance,temperature,power_mode):
        self.age.append(age)
        self.angle_x.append(angle1)
        self.angle_y.append(angle2)
        self.angle_z.append(angle3)
        #self.distance_to_sun.append(distance)
        self.temperature.append(temperature)
        self.power_mode.append(power_mode)



#arrays over time (deliverables)
# angle_sun_earth=[angle_sun_earth]
# angle_earth_sat=[angle_earth_sat]
# Distance_satellite_sun=[]



##Calculate Orbit time satellite
#T_orbit=math.sqrt(4*(math.pi)**2*R_tot**3/(G*M_eart))

##Calulate Obit time earth
#T_orbit_eart=math.sqrt(4*(math.pi)**2*earth_sun**3/(G*M_sun))


def calculate_angles(t,satellite,idx):
    #orbit
    # angle_sun=360*(t%T_orbit_eart)/T_orbit_eart
    # angle_sun_earth.append(angle_sun)
    # angle_sat=360*(t%T_orbit)/T_orbit
    # angle_earth_sat.append(angle_sat)
    ##Calculate distance sun - satellite
    # angle=180+angle_sun_earth[-1]-angle_earth_sat[-1]
    # #Kosinussatz
    # dist=math.sqrt(earth_sun**2+R_tot**2-2*earth_sun*R_tot*math.cos(angle/180*math.pi))
    # Distance_satellite_sun.append(dist)
    # satellite.distance_to_sun.append(dist)
    # satellite.angle_to_sun.append(angle_sun+math.asin(R_tot/dist)*180/math.pi)


    dist=math.sqrt(float(orbit_x_sat[idx])**2+float(orbit_y_sat[idx])**2+float(orbit_z_sat[idx])**2)
    sat_sun_x=float(orbit_x_sat[idx])/dist
    sat_sun_y=float(orbit_y_sat[idx])/dist
    sat_sun_z=float(orbit_z_sat[idx])/dist
    satellite.orbit_x.append(sat_sun_x)
    satellite.orbit_y.append(sat_sun_y)
    satellite.orbit_z.append(sat_sun_z)

def calculate_satellite_angles(satellite):
    rot_x=satellite.rotational_speed_x[-1]
    rot_y=satellite.rotational_speed_y[-1]
    rot_z=satellite.rotational_speed_z[-1]
    angle_x_new=satellite.angle_x[-1]+time_step*rot_x
    angle_y_new=satellite.angle_y[-1]+time_step*rot_y
    angle_z_new=satellite.angle_z[-1]+time_step*rot_z
    satellite.angle_x.append(angle_x_new)
    satellite.angle_y.append(angle_y_new)
    satellite.angle_z.append(angle_z_new)

#returns if possible to transmit data to earth or not
def check_for_transmition_window(idx):
    ans=0
    if abs(float(orbit_lat[idx])-ground_station_lat)<ground_station_radius and abs(float(orbit_lon[idx])-ground_station_lon)<ground_station_radius:
        ans=1
    return ans
