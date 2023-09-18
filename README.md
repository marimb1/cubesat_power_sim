# Simulation Tool for the Power System of Nanosatellites

## Description

ARIS (Akademische Raumfahrtsinitative Schweiz) plans to
launch a cubesat into low earth orbit in 2025. The aim is
to be able to study human cells in weightlessness. The 3U
cubesat contains a small microscope to examine the human
cells continuously in space. In order for the cells to survive
at all, many conditions must be maintained, such as a relatively
narrow temperature range. Therefore, the cells must
be constantly monitored and heated, or cooled. For technical
reasons, the cubesat only has non-folding solar panels on three
major sides. Due to the energy consumption of the cubesat and
the limited energy harvesting, the design of the electric power
system of the cubesat is a key point. The goal of this work is to
develop a simulation software in order to verify the electrical
power system of the cubesat. This includes in particular the
capacity of the battery, the energy harvesting and the energy
consumption.

## How to Run a Simulation

The simulation is divided into three parts. This has the advantage that all three parts
must not always be carried out.

- [ ] Orbit Simulation
- [ ] Power Simulation (main simulation)
- [ ] Plotting the Results

The orbit simulation and the power simulation have a relatively long runtime (a few minutes).
Most of the time you run several simulations for the same orbit, that way it is
not necessary to simulate the orbit each time. Also, saving the output of the data first
seems to make a lot of sense since additional plots may need to be created at a later time
or plots may need to be changed.

### 1. Import Orbit Files

This section only has to be performed when a new orbit is added.

In order to simulate any orbit, an orbit TLE set must be imported. This TLE set can
either be calculated by the user or found on the Internet.

The TLE set is to be added to the file *Orbit/orbit_tle.txt*

### 2. Simulate Orbit

This step only has to be performed if the orbit parameters have changed or a new orbit is added.

In the document *Orbit/variables.py* the orbit parameters must be set as follows:

Variable | Description
---------|------------
do_orbit_simulation | If true, the orbit simulation is performed
orbit_t_step | Set the orbit simulation timestep
year | Set the simulation start year
month | Set the simulation start month
day | Set the simulation start day
hour | Set the simulation start hour
minute | Set the simulation start minute
second | Set the simulation start second
microsecond | Set the simulation start microsecond
max_orbit_time | Set the maximum orbit simulation time in seconds
tle_file | Set the location of the TLE file
orbit_name | Set the orbit name, has to match with the TLE entry
csv_file_name_out_orbit | Set the name of the orbit output CSV file
csv_file_to_use | Set the orbit file to use for the simulation

If no orbit simulation is to be performed, the variable do_orbit_simulation must be set
to False. In this case, only the variable csv_file_to_use is used, which specifies the
path to the orbit file to be used. All other orbit variables are obsolete in this case.

The variable orbit_t_step sets the timestep for the orbit simulation. This timestep does
not have to match the timestep of the simulation. It may make sense to choose a larger
timestep for the orbit simulation than for the power simulation.

The variables year, month, day, hour, minute, second and microsecond are used to
define the exact starting point of the orbit simulation. For the start of the power simulation,
the same starting point is used.

The maximum orbit simulation time is determined with the variable max_orbit_time.
This value must be greater than or equal to the power simulation duration.

The variables tle_file, csv_file_name_out_orbit and csv_file_to_use are the paths
to the corresponding files. The name of the TLE set to simulate must be the same as
the name orbit_name.

### 3. Set Simulation Parameters

The main control panel of the power simulation is the *variables.py* file. Here all parameters can be set.

#### Main Simulation Parameters

Variable | Description
---------|------------
time_step | Time step for power simulation
max_simulation_time | Set the maximum simulation time for the power simulation

#### Battery Parameters

Variable | Description
---------|------------
Cells_in_Series | Batterie cells in series
E0 | Constant voltage of the battery
K | Voltage/Capacity in the linear region
Q | Batterie capacity
Q_act | Actual charge state
A | Exponential zone variable
B | Exponential zone variable
R_nom | Battery internal resistance
battery_critical_voltage | Set the critical voltage threshold
battery_emergency_voltage | Set the emergency voltage threshold

Most battery variables can be obtained from the battery’s datasheet or by simple calculations.

#### Ground Station Parameters

Variable | Description
---------|------------
ground_station_lon | Ground station longitude in degree
ground_station_lat | Ground station latitude in degree
ground_station_radius | Ground station transmission radius in degree

The ground station variables contain the position of the ground station. These are
needed to simulate the transmission windows. The ground_station_radius defines in
which radius around the ground station a transmission to the satellite is possible.

#### CubeSat Parameters

Variable | Description
---------|------------
angle_1 | Initial x angle of the satellite in degree
angle_2 | Initial y angle of the satellite in degree
angle_3 | Initial z angle of the satellite in degree
rotational_speed_x | Initial rotational speed around x-axis in degree per second
rotational_speed_y | Initial rotational speed around y-axis in degree per second
rotational_speed_z | Initial rotational speed around z-axis in degree per second
rot_correction_speed_x | Correction speed in x direction in degree per second
rot_correction_speed_y | Correction speed in y direction in degree per second
rot_correction_speed_z | Correction speed in z direction in degree per second

These variables define the initial position and the rotation of the satellite. The position variables angle_1, angle_2 and angle_3 are in relation to the sun.

#### Solar Panel Parameters

Variable | Description
---------|------------
solarpanel_1_power | Initial power of solar panel 1
solarpanel_2_power | Initial power of solar panel 2
solarpanel_3_power | Initial power of solar panel 3
health_panel1 | Initial health of solar panel 1
health_panel2 | Initial health of solar panel 2
health_panel3 | Initial health of solar panel 3
panel_defect | Defect of a panel at a specific time

The maximum power of the solar panels is specified directly for space. This power is
higher than on earth, because there is no atmosphere. The power in low Earth orbit can
be found in the datasheet for space-proven solar panels. The initial health of the solar
panels can also be specified. Here, a possible defect of a solar panel can be simulated.
The value must be between 1 and 0, where 1 means that the solar panel is fully operational.
The variable panel_defect is a list of tuples, where the tuples are of the form
(time, defect_p1, defect_p2, defect_p3) where defect_p1 is the percentage of panel 1
that should fail at this time. If a panel is to fail multiple times, the percentage is always
applied to the current state.

#### Duration of Operations

Variable | Description
---------|------------
deploy_max_duration | Duration of the antenna deployment
test_max_duration | Duration of initial equipment test
test_tx | Duration of the initial transmission
GPS_measurement_duration | Duration of a GPS measurement
Split_time | Time between two splits
Split_duration | Duration of a split
Tx_time | Duration of one transmission
Rx_time | Duration of one receiving

The duration of the individual operations can be changed here by changing the corresponding
variables.

### 4. Start Simulation

After setting all parameters, the simulation can be started by executing the script main_simulation.py.

The simulation now takes a while and saves all values in the folder simulation_output
as a CSV file in the folder *simulation_output*. The CSV file is numbered consecutively. It is recommended to rename
the document after the simulation.

### 5. Plotting Results

After the simulation has been performed, all values are stored in the corresponding CSV
file. These values can now be used to generate different plots.

In the file simulation_output/plots.py, the reading of the CSV file is already preprogrammed as well as some
basic plots. However, all arbitrary desired plots can be generated.

## Future Work

### Battery Model

The battery model seems to match the tested battery very well. It might be worth
creating a library to make the battery model accessible to others. First, however, further
tests with other batteries would have to be carried out in the laboratory to check whether
the deviation from the simulation is small. The timeframe of this thesis was also not
sufficient to carry out a long-term test of battery degradation and to compare it with the
simulation model.

### Orbit Model

The orbit model is mostly based on an external Python library. This works fine. However,
it would be preferable if the calculations of the required data could be performed
without this external library, then the entire simulation would be independent of external
libraries.

### Runtime of the Simulation

The simulation delivers all the desired results, but in order to keep the runtime within
a reasonable range, the simulation step size has to be increased to around 60 seconds.
For the rough analysis of the mission, this step size is sufficient, but if a detailed analysis
should be necessary, a smaller step size may be necessary. It would therefore be good
if the individual parts of the simulation were examined and improved for possible weak
points regarding the runtime.