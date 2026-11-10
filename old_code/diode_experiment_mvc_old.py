## NOAH ZEEMAN - 15494365
## NSP2 - ECPC - Model-View-Controller "Pythondaq: model en view afsplitsen"
## 10 Nov '26


# import necessary packages
import pyvisa
import statistics as stats
from math import sqrt
import csv
from pathlib import Path
from arduino_device import ArduinoVISADevice, list_resources
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

# turn off Arduino
device.set_output_voltage(0)


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