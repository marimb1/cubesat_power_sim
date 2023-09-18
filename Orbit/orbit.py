from datetime import datetime, timedelta
import math
import skyfield
from skyfield.api import load, wgs84,utc
import csv
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
sys.path.append('..')


'''
Calculated the orbit data for a given orbit and saves the output in a csv file

Input:
timestep : orbit simulation timestep
starttime: first calculation time
orbit_name: name of the satellite orbit (Has to match the TLE element name)
max_sim_time: Maximum orbit simulation time in seconds
orbit_file: Location of the TLE data file (.txt)
output_name: name of the output csv file

Output:
A csv file with the following content:
THE FIRST TWO ROWS ARE FOR ADDITIONAL INFORMATIONS AND DOES NOT CONTAIN ANY CALCULATIONS:
1. Row: timestep,starttime
2. Row: Description of following colums
Data rows: deltatime,x_sat,y_sat,z_sat,sat_in_sun,earth_sun,sat_pos,sun_sat_pos,lat,lon,height
'''

def orbit_calculation(timestep=300,starttime=datetime(2023,6,7,13,15,0,0,utc),orbit_name='ISS',max_sim_time=100,orbit_file='./Orbit/orbit_tle.txt',output_name='standard.csv'):
    print('Loading orbit %s...'%orbit_name)
    satellites = load.tle_file(orbit_file)
    by_name = {sat.name: sat for sat in satellites}
    sat=by_name[orbit_name]
    planets = load('./Orbit/de421.bsp')  # ephemeris DE421
    earth = planets['Earth']
    sun = planets['Sun']
    
    #Set time for calculations
    print('Set simulation timestep to %d and maximum simulation time to %d'%(timestep,max_sim_time))
    ts = load.timescale()
    delta=timedelta(0,timestep)
    d=starttime

    t_a=[]
    time_a=[]
    earth_sun=[]
    sat_pos=[]
    sun_sat_pos=[]
    sat_in_sun=[]
    lat_a=[]
    lon_a=[]
    height=[]

    for i in range(0,int(max_sim_time/timestep)+1):
        t = ts.from_datetime(d+i*delta)
        time_a.append(t)
        time=i*delta
        t_a.append(time.total_seconds())

        #Calulate Geocentric satellite position
        satellite_position_geocentric = sat.at(t)
        lat,lon=wgs84.latlon_of(satellite_position_geocentric)
        lat_a.append(lat.degrees)
        lon_a.append(lon.degrees)
        height.append(wgs84.height_of(satellite_position_geocentric).m)
        sat_pos.append(satellite_position_geocentric.position.m)

        #Calculate if satellite is in sun
        in_sun=satellite_position_geocentric.is_sunlit(planets)
        sat_in_sun.append(in_sun)

        #Calculate earth position with respect to sun (With Barycenter of solar system)
        sun_pos=sun.at(t)
        earth_from_sun_position = sun_pos.observe(earth)
        earth_sun.append(earth_from_sun_position.position.m)

        #Calculate Satellite position with respect to sun
        sun_sat_pos_e = earth_from_sun_position.position.m+satellite_position_geocentric.position.m
        sun_sat_pos.append(sun_sat_pos_e)

   
    #Geocentric satellite position
    x_sat=[]
    y_sat=[]
    z_sat=[]

    #Plot satellite Orbit
    for i in sun_sat_pos:
        x_sat.append(i[0])
        y_sat.append(i[1])
        z_sat.append(i[2])

    def plot_3D():
        fig=plt.figure(figsize=(8,8))
        ax = fig.add_subplot(projection='3d')
        # ax.scatter(x_sat, y_sat, z_sat, label='Satellite Orbit')
        # ax.legend()


        # ax.set_xlabel('X')
        # ax.set_ylabel('Y')
        # ax.set_zlabel('Z')

        # ax.view_init(elev=20., azim=-35, roll=0)

        # plt.show()


        #Plot Earth orbit

        x=[]
        y=[]
        z=[]


        for i in earth_sun:
            x.append(i[0])
            y.append(i[1])
            z.append(i[2])

        x_anim=[]
        y_anim=[]
        z_anim=[]

        x_earth=[]
        y_earth=[]
        z_earth=[]
        
        #ax.scatter(x, y, z, label='Earth Orbit')
        earth=ax.plot(x,y,z, label='Earth Orbit')
        #ax.scatter(x_sat, y_sat, z_sat, label='Satellite Orbit')
        line=ax.plot(x_anim, y_anim, z_anim, label='Satellite Orbit')
        ax.legend()
        def update(frame,line):
            line.set_data(x_sat[:frame],y_sat[:frame])
            line.set_3d_properties(z_sat[:frame])
            # earth.set_data(x[:frame],y[:frame])
            # earth.set_3d_properties(z[:frame])
            return line,earth
        
     
        ax.set_xlabel('X [m]')
        ax.set_ylabel('Y [m]')
        ax.set_zlabel('Z [m]')

        ax.view_init(elev=20., azim=-35, roll=0)
        #plt.savefig('orbit_sat_earth_iss.pdf')
        ani = animation.FuncAnimation(fig=fig,func=update,frames=len(x_sat),fargs=(line),interval=100)
        #ani.save('animation_earth_sat.gif',writer='imagemagick', fps=60)
        plt.show()

    def plot_3D_earth():
        fig=plt.figure(figsize=(8,8))
        ax = fig.add_subplot(projection='3d')
        # ax.scatter(x_sat, y_sat, z_sat, label='Satellite Orbit')
        # ax.legend()


        # ax.set_xlabel('X')
        # ax.set_ylabel('Y')
        # ax.set_zlabel('Z')

        # ax.view_init(elev=20., azim=-35, roll=0)

        # plt.show()


        #Plot Earth orbit

        x=[]
        y=[]
        z=[]


        for i in earth_sun:
            x.append(i[0])
            y.append(i[1])
            z.append(i[2])

        x_anim=[]
        y_anim=[]
        z_anim=[]

        x_earth=[]
        y_earth=[]
        z_earth=[]
        
        #ax.scatter(x, y, z, label='Earth Orbit')
        earth=ax.plot(x,y,z, label='Earth Orbit')
        #ax.scatter(x_sat, y_sat, z_sat, label='Satellite Orbit')
        sat=ax.plot(x_sat, y_sat, z_sat, label='Satellite Orbit')
        ax.legend()
        def update(frame,earth,sat):
            earth=earth[0]
            sat=sat[0]
            earth.set_data(x[:frame],y[:frame])
            earth.set_3d_properties(z[:frame])
            sat.set_data(x_sat[:frame],y_sat[:frame])
            sat.set_3d_properties(z_sat[:frame])
            return earth,sat
        
     
        ax.set_xlabel('X [Mio. km]',fontsize=12)
        ax.xaxis.set_tick_params(labelsize=10)
        ax.set_xticklabels(['',-36.1,'','','','',-35.6,'',])
        ax.set_yticklabels(['',-135.42,'','','','','','',-135.53,'',])
        ax.set_zticklabels(['',-58.70,'','','','',-58.65,'',])
        ax.set_ylabel('Y [Mio. km]',fontsize=12)
        ax.yaxis.set_tick_params(labelsize=10)
        ax.set_zlabel('Z [Mio. km]',fontsize=12)
        ax.zaxis.set_tick_params(labelsize=10)

        ax.view_init(elev=20., azim=-35, roll=0)
        plt.savefig('animation_earth_sat_both.pdf')
        ani = animation.FuncAnimation(fig=fig,func=update,frames=len(x),fargs=(earth, sat),interval=100)
        writervideo  = animation.FFMpegWriter(fps=60)
        ani.save('animation_earth_sat_both.gif')
        plt.show()

    def plot_3D_from_earth():
        fig=plt.figure(figsize=(8,8))
        ax = fig.add_subplot(projection='3d')
        # ax.scatter(x_sat, y_sat, z_sat, label='Satellite Orbit')
        # ax.legend()


        # ax.set_xlabel('X')
        # ax.set_ylabel('Y')
        # ax.set_zlabel('Z')

        # ax.view_init(elev=20., azim=-35, roll=0)

        # plt.show()


        #Plot Earth orbit

        x=[]
        y=[]
        z=[]


        for i in earth_sun:
            x.append(i[0])
            y.append(i[1])
            z.append(i[2])

        x_anim=[]
        y_anim=[]
        z_anim=[]

        x_earth=[]
        y_earth=[]
        z_earth=[]
        
        #ax.scatter(x, y, z, label='Earth Orbit')
        #earth=ax.plot(x,y,z, label='Earth Orbit')
        #ax.scatter(x_sat, y_sat, z_sat, label='Satellite Orbit')
        sat=ax.plot(x_sat, y_sat, z_sat, label='Satellite Orbit')
        ax.plot(4709.227185118779,-5831.1154831680105,-10490.318926979866,label='Earth',marker="o", markersize=20,color='green')
        ax.legend()
        def update(frame,sat):
            #sat=sat[0]
            sat.set_data(x_sat[:frame],y_sat[:frame])
            sat.set_3d_properties(z_sat[:frame])
            return sat
        
     
        ax.set_xlabel('X [Tsd. km]',fontsize=12)
        ax.xaxis.set_tick_params(labelsize=10)
        ax.set_xticklabels(['',-6,'','',0,'','',6,'',])
        ax.set_yticklabels(['',-4,'',0,'',4,'',])
        ax.set_zticklabels(['',-4,'',0,'',4,'',])
        ax.set_ylabel('Y [Tsd. km]',fontsize=12)
        ax.yaxis.set_tick_params(labelsize=10)
        ax.set_zlabel('Z [Tsd. km]',fontsize=12)
        ax.zaxis.set_tick_params(labelsize=10)

        ax.view_init(elev=20., azim=-35, roll=0)
        plt.savefig('animation_from_earth.pdf')
        ani = animation.FuncAnimation(fig=fig,func=update,frames=len(x),fargs=(sat),interval=100)
        # writervideo  = animation.FFMpegWriter(fps=60)
        ani.save('animation_from_earth.gif')
        plt.show()
        
    def plot_sunlight():
        plt.plot(t_a,sat_in_sun)
        plt.title('Asnaro Satellite sunlight time')
        plt.savefig('Asnaro_sat_sunlight.pdf')
        plt.show()

    def write_csv():
        saveloc='./Orbit/%s'%output_name
        with open(saveloc, 'w',newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestep,starttime])
            writer.writerow(['timestep=%d'%timestep,'x_sat','y_sat','z_sat','sat_in_sun','earth_sun','sat_pos','sun_sat_pos','lat','lon','height'])
            for idx,element in enumerate(t_a):
                writer.writerow([t_a[idx],x_sat[idx],y_sat[idx],z_sat[idx],sat_in_sun[idx],earth_sun[idx],sat_pos[idx],sun_sat_pos[idx],lat_a[idx],lon_a[idx],height[idx]])
        print('csv file written..')
            
    #plot_3D_earth()
    write_csv()

orbit_calculation(max_sim_time=20000)