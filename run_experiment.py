## NOAH ZEEMAN - 15494365
## NSP2 - ECPC - Model-View-Controller "Pythondaq: model en view afsplitsen"
## 10 Nov '26


# import necessary packages
from diode_experiment import DiodeExperiment, list_resources
import csv
from pathlib import Path

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

# connect to Arduino via class DiodeExperimemnt
device= DiodeExperiment(port="ASRL/dev/ttyACM0::INSTR")

# get average voltage, average current, error average voltage and error average current from method scan(start, stop, repeat)
u_avg, u_err, I_avg, I_err= device.scan(0, 3.31, 6)

# print average voltage: average_voltage_LED +/- err_average_voltage_LED V  average current: average_current_LED +/- err_average_current_LED A
print(
    f"gemiddelde spanning LED: {u_avg[-1]:.4f} +/- {u_err[-1]:.4f} V\n"
    f"gemiddelde stroomsterkte LED: {I_avg[-1]:.4f} +/- {I_err[-1]:.4f} mA" 
)

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