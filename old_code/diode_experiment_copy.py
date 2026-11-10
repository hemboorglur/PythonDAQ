## NOAH ZEEMAN - 15494365
## NSP2 - ECPC - basisscript voor het experiment "csv"
## 3 Nov '26


# import necessary packages
import pyvisa
import statistics as stats
from math import sqrt
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
plt.rcParams["webagg.address"] = "10.42.0.1"
plt.rcParams["webagg.port"] = 8988
plt.rcParams["webagg.open_in_browser"] = False



# connect to Arduino
rm = pyvisa.ResourceManager("@py")
ports = rm.list_resources()

arduino = rm.open_resource(
    "ASRL/dev/ttyACM0::INSTR", read_termination="\r\n", write_termination="\n"
)


# set constants
R_ohm, C_adc_vol = 220, 3.3/1023


# set lists:
u_LED, I_LED= [], []
u_avg, I_avg= [], []
u_err, I_err= [], []


# set output voltage form 0 to max
# --set number of repeated measurements

repeats = 2**3

# chose the 'turtle'-method:
# sets the light-level, measures that level repeatedly and sets the next light-level

for i in range(2**10):
    arduino.query(f"OUT:CH0 {i}")
    for rep in range(repeats):

        # measure voltages 
        u1_adc, u2_adc= int(arduino.query("MEAS:CH1?")), int(arduino.query("MEAS:CH2?"))

        # calculate voltages
        u1_vol, u2_vol= C_adc_vol * u1_adc, C_adc_vol * u2_adc

        # calculate current & voltage LED (and append to list)
        u_LED.append(u1_vol - u2_vol)
        I_LED.append(( u2_vol / R_ohm )* 1000)

    
    # delete all list items except from current repeat
    # take the average and standarddeviation using Python Standard Library module Statistics
    # append to respective lists

    # calculate average voltage LED and uncertainty
    del u_LED[:-repeats]
    u_avg.append(stats.mean(u_LED))
    u_err.append((stats.stdev(u_LED)) / sqrt(repeats))

    # calculate average current LED and uncertainty
    del I_LED[:-repeats]
    I_avg.append(stats.mean(I_LED))
    I_err.append((stats.stdev(I_LED)) / sqrt(repeats))


# turn LED off
light_off = arduino.write(f"OUT:CH0 0")
arduino.close()


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