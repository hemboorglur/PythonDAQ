## NOAH ZEEMAN - 15494365 - Universiteit van Amsterdam
## NSP2 - ECPC - Model-View-Controller "Pythondaq: controller implementeren"
## 10 Nov '26


# import necessary packages
import pyvisa
import statistics as stats
from math import sqrt
import csv
from pathlib import Path
import numpy as np


# hash these lines for normal plt.show() rendering
import matplotlib
matplotlib.use("WebAgg")

# don't hash this line, has to import after setting a webserver
import matplotlib.pyplot as plt

# hash these lines for normal plt.show() rendering
# Raspberry Pi OS Lite can't display graphs, 
# so set a webserver that can render graphs in an external webbrowser
plt.rcParams["webagg.address"] = "0.0.0.0"
plt.rcParams["webagg.port"] = 8988
plt.rcParams["webagg.open_in_browser"] = False


# list available Ardiunos
def list_resources():
    return pyvisa.ResourceManager("@py").list_resources()


class ArduinoVISADevice:
    # constants used within the class
    C_adc_vol, C_vol_adc = 3.3/1023, 1023/3.3

    def __init__(self, port):
        self.arduino= pyvisa.ResourceManager("@py").open_resource(port, read_termination="\r\n", write_termination="\n")
    
    def get_identification(self):
        return self.arduino.query("*IDN?")

    def set_output_value(self, value):
        self.arduino.query(f"OUT:CH0 {value}")
        return f"{value}"

    def set_output_voltage(self, voltage):
        self.set_output_value(int(voltage * self.C_vol_adc))
        return f"{voltage:.2f} V"

    def get_output_value(self):
        return self.arduino.query(f"OUT:CH0?")

    def get_output_voltage(self, channel):
        return f"{self.C_adc_vol * self.get_output_value():.2f}"

    def get_input_value(self, channel):
        return int(self.arduino.query(f"MEAS:CH{channel}?"))

    def get_input_voltage(self, channel):
        return f"{self.get_input_value(channel) * self.C_adc_vol:.2f}"


# get list resources
print(list_resources())

# connect to Arduino via class ArduinoVISADevice
device= ArduinoVISADevice(port="ASRL/dev/ttyACM0::INSTR")


# set constants
R_ohm, C_adc_vol = 220, 3.3/1023

# set lists:
u_LED, I_LED= [], []
u_avg, I_avg= [], []
u_err, I_err= [], []

# set repeats
repeats= 3

for i in np.arange(0, 3.3, 0.01):
    print(device.set_output_voltage(i))
    for rep in range(repeats):
        u_1, u_2= float(device.get_input_voltage(1)), float(device.get_input_voltage(2))
        u_LED.append(u_1 - u_2)
        I_LED.append(u_2 / R_ohm *1000)

    del u_LED[:-repeats]
    u_avg.append(stats.mean(u_LED))
    u_err.append((stats.stdev(u_LED)) / sqrt(repeats))

    del I_LED[:-repeats]
    I_avg.append(stats.mean(I_LED))
    I_err.append((stats.stdev(I_LED)) / sqrt(repeats))

device.set_output_voltage(0)




# set output voltage from 0 to 3.3
#   set number of repeated measurements
#       measure voltages
#       calculate voltage LED
#       calculate current LED
#   calculate average voltage LED and uncertainty
#   calculate average current LED and uncertainty
#   print average voltage: average_voltage_LED +/- err_average_voltage_LED V  average current: average_current_LED +/- err_average_current_LED A
#
# turn LED off
# create csv-file
# plot average_current_LED vs average_voltage_LED



# create csv-file
header= ['raw_value', 'u_avg (V)', 'u_err (V)', 'I_avg (mA)', 'I_err (mA)']

# check if file already exists, sets name accordingly
folder, n= Path("ECPC/PythonDAQ"), 1
while (folder / f"data-{n}.csv").exists(): n+= 1
filename= (folder / f"data-{n}.csv")

# write information to file
with open(filename, "w", newline="") as datafile:
    writer= csv.writer(datafile)
    writer.writerow(header)
    for a, b, c, d, e in zip(range(pow(2,10)), u_avg, u_err, I_avg, I_err):
        writer.writerow([a, b, c, d, e])
datafile.close()

# plot average_current_LED vs average_voltage_LED
plt.errorbar(u_avg, I_avg, xerr= u_err, yerr= I_err, fmt=".", capsize=2,)

plt.xlabel("LED voltage (V)")
plt.ylabel("LED stroomsterkte (mA)")
plt.title("I tegen U uitgezet")

plt.grid()
plt.show()