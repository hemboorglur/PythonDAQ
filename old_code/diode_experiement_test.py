 ## NOAH ZEEMAN - 15494365
## NSP2 - ECPC - basisscript voor het experiment "csv"
## 3 Nov '26


# importeren van benodigde packages
import pyvisa
import statistics as stats
from math import sqrt
import csv
from pathlib import Path
import matplotlib
matplotlib.use("WebAgg")
import matplotlib.pyplot as plt


# instellen van een webserver waar matplotlib de grafieken kan weergeven
plt.rcParams["webagg.address"] = "10.42.0.1"
plt.rcParams["webagg.port"] = 8988
plt.rcParams["webagg.open_in_browser"] = False


# connect to Arduino
rm = pyvisa.ResourceManager("@py")
ports = rm.list_resources()
#print(ports)

arduino = rm.open_resource(
    "ASRL/dev/ttyACM0::INSTR", read_termination="\r\n", write_termination="\n"
)
#print(arduino.query("*IDN?"))

### specificaties:
# bereik voltage 0.0 V - 3.3 V
# bereik raw_value 0 - 1023 (1024 = 2^10)
# dus: voltage = (max_voltage / max_raw_value) * raw_value
# weerstand van 220ohm in serie geschakeld met een LED
# zenden naar kanaal 0 (CH0)
# ontvangen uit kanaal 1 (CH1) & kanaal 2 (CH2)

# u1 = u_LED + u_weerstand
# u2 = u_weerstand
# volgens de wet v/Kirchoff:    u_LED = u_1 - u_2
# volgens de wet v/Ohm:         I_LED = u_2 / R 

# constante omrekenenings-waardes:
C_adc_vol= 3.3/1023
R_ohm= 220

# lijsten voor de spannings- en stroomsterkte- waardes, 
# en de gemiddelde waarden voor de spanning en stroomsterkte,
# en de onzekerheid voor de spanning en stroomsterkte 
u_LED, I_LED= [], []
u_avg, I_avg= [], []
u_err, I_err= [], []


# set output voltage form 0 to max
# --set number of repeated measurements

repeats = int(3)

# schildpad methode gekozen (de computer doet toch het werk ;D)

for i in range(pow(2,10)):
    light_i = arduino.query(f"OUT:CH0 {i}")

    for rep in range(repeats):

        # measure voltages
        u1_adc, u2_adc= int(arduino.query("MEAS:CH1?")), int(arduino.query("MEAS:CH2?"))

        # calculate voltages
        u1_vol, u2_vol= C_adc_vol * u1_adc, C_adc_vol * u2_adc

        # calculate current & voltage LED (and append to list)
        u_LED.append(u1_vol - u2_vol)
        I_LED.append(( u2_vol / R_ohm )* 1000)

        # print voltage: voltage_LED V (raw_voltage_LED) current: current_LED A
        #print(
        #    f"ruwe waarde spanning LED: {u1_adc - u2_adc} ({u_LED[-1]} V)\n"
        #    f"ruwe waarde spanning weerstand: {u2_adc} ({u2_vol} V)\n"
        #    f"stroomsterkte LED: {I_LED[-1]} mA"
        #)


    # haal de laatste metingswaarden uit de lijst, neem het gemiddelde, voeg die waarde toe aan de lijst met gemiddelden
    # herhaal voor standaarddeviatie
    
    # calculate average voltage LED and uncertainty
    del u_LED[:-repeats]
    u_avg.append(stats.mean(u_LED))
    u_err.append((stats.stdev(u_LED)) / sqrt(repeats))

    # calculate average current LED and uncertainty
    del I_LED[:-repeats]
    I_avg.append(stats.mean(I_LED))
    I_err.append((stats.stdev(I_LED)) / sqrt(repeats))


    # print average voltage: average_voltage_LED +/- err_average_voltage_LED V  average current: average_current_LED +/- err_average_current_LED A
    #print(
    #    f"gemiddelde spanning LED: {u_avg[-1]:.4f} +/- {u_err[-1]:.4f} V\n"
    #    f"gemiddelde stroomsterkte LED: {I_avg[-1]:.4f} +/- {I_err[-1]:.4f} mA" 
    #)

# turn LED off
light_off = arduino.write(f"OUT:CH0 0")
arduino.close()


# create csv-file
header= ['raw_value', 'u_avg (V)', 'u_err (V)', 'I_avg (mA)', 'I_err (mA)']

# check of bestand al bestaat
folder, n= Path("ECPC/PythonDAQ"), 1
while (folder / f"data-{n}.csv").exists(): n+= 1
filename= (folder / f"data-{n}.csv")

# informatie naar bestand schrijven    
with open(filename, "w", newline="") as datafile:
    writer= csv.writer(datafile)
    writer.writerow(header)
    for a, b, c, d, e in zip(range(pow(2,10)), u_avg, u_err, I_avg, I_err):
        writer.writerow([a, b, c, d, e])
datafile.close()


# plot current_LED vs voltage_LED
# --> plot average_current_LED vs average_voltage_LED

#plt.scatter(u_LED, I_LED, s=8)

plt.errorbar(
    u_avg,
    I_avg,
    xerr= u_err,
    yerr= I_err,
    fmt=".",
    capsize=2,
)

plt.xlabel("LED voltage (V)")
plt.ylabel("LED stroomsterkte (mA)")
plt.title("I tegen U uitgezet")

#plt.xlim(1.75, 1.80)
#plt.ylim(1.0, 2.0)

plt.grid()
plt.show()