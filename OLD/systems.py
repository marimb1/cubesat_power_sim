
class subsystems:
    def __init__(self,power,active_in):
        self.powerconsumption={"Detumble":power[0],
                               "Deploy":power[1],
                               "Test":power[2],
                               "Tx_Test":power[3],
                               "Charge":power[4],
                               "Split":power[5],
                               "Point":power[6],
                               "Desaturation":power[7],
                               "Tx":power[8],
                               "Rx":power[9],
                               "Spin Up":power[10],
                               "Experiment":power[11],
                               "Spin Down":power[12],
                               "Beacon":power[13],
                               "Critical":power[14],
                               "Emergency":power[15]   
                                }
        self.active_in_mode={"Detumble":active_in[0],
                               "Deploy":active_in[1],
                               "Test":active_in[2],
                               "Tx_Test":active_in[3],
                               "Charge":active_in[4],
                               "Split":active_in[5],
                               "Point":active_in[6],
                               "Desaturation":active_in[7],
                               "Tx":active_in[8],
                               "Rx":active_in[9],
                               "Spin Up":active_in[10],
                               "Experiment":active_in[11],
                               "Spin Down":active_in[12],
                               "Beacon":active_in[13],
                               "Critical":active_in[14],
                               "Emergency":active_in[15]   
                                }
        self.total_powerconsumption=0
        self.actual_power_consumption=[]

def total_consumption(subsystems,powermode):
    P_tot=0
    for sub in subsystems:
        
        if sub.powerconsumption[powermode]!='x':
            P_tot=P_tot+float(sub.powerconsumption[powermode])
    return P_tot