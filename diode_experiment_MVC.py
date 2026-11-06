## NOAH ZEEMAN - 15494365 - Universiteit van Amsterdam
## NSP2 - ECPC - Model-View-Controller "Pythondaq: controller bouwen"
## 6 Nov '26


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


# def list_resources
#    return list of available ports
#
# class ArduinoVISADevice:
#    def __init__ (ask port from user)
#        open device
#
#    def get_identification
#        return identification string of connected device
#
#   def set_output_value
#        set a value on the output channel and return the Arduino's response
#
#   def set_output_voltage
#        set a voltage on the output channel (in Volt) and return the Arduino's response
#
#   def get_output_value
#        return the value of the output channel
#
#   def get_output_voltage
#        return the voltage of the output channel (in Volt)
#      
#   def get_input_value
#        return the value of the input channel
#
#   def get_input_voltage
#        return the voltage of the input channel (in Volt)

### einde pseudo code

def list_resources():
    # connect to Arduino
    rm= pyvisa.ResourceManager("@py")
    return print(rm.list_resources())


class ArduinoVISADevice:
    R_ohm, C_adc_vol, C_vol_adc = 220, 3.3/1023, 1023/3.3

    def __init__(self, port):
        self.arduino= pyvisa.ResourceManager("@py").open_resource(port, read_termination="\r\n", write_termination="\n")
    
    def get_identification(self):
        return self.arduino.query("*IDN?")

    def set_output_value(self, value):
        return self.arduino.query(f"OUT:CH0 {value}")
        
    def set_output_voltage(self, voltage):
        self.output_value= int(voltage * self.C_vol_adc)
        self.output_voltage= voltage
        self.set_output_value(self.output_value)
        return f"set output to {self.output_voltage}"

    def get_output_value(self):
        return self.output_value

    def get_output_voltage(self):
        return self.output_voltage

    def get_input_value(self, channel):
        return int(self.arduino.query(f"MEAS:CH{channel}?"))

    def get_input_voltage(self, channel):
        return f"{self.get_input_value(channel) * self.C_adc_vol} V"

    

# get available ports
print(list_resources())

# create an instance for the Arduino on port "ASRL28::INSTR"
# port for testing: "ASRL/dev/ttyACM0::INSTR"
device = ArduinoVISADevice(port="ASRL/dev/ttyACM0::INSTR")


# print identification string
identification = device.get_identification()
print(identification)

# set OUTPUT voltage on channel 0 in Volt (0 - 3.3 V)
response = device.set_output_voltage(voltage=3.3)
print(f"{response=}")

# set OUTPUT voltage on channel 0 in ADC values (0 - 1023)
device.set_output_value(value=828)

# measure the voltage on INPUT channel 2 in ADC values (0 - 1023)
ch2_value = device.get_input_value(channel=2)
print(f"{ch2_value=}")

# measure the voltage on INPUT channel 2 in Volt (0 - 3.3 V)
ch2_voltage = device.get_input_voltage(channel=2)
print(f"{ch2_voltage=}")

# get the previously set OUTPUT voltage on channel 0 in ADC values (0 - 1023)
ch0_value = device.get_output_value()
print(f"{ch0_value=}")

# turn of the LED
device.set_output_voltage(voltage=0)

### einde test code








# # set constants
# R_ohm, C_adc_vol = 220, 3.3/1023


# # set lists:
# u_LED, I_LED= [], []
# u_avg, I_avg= [], []
# u_err, I_err= [], []


# # set output voltage form 0 to max
# # --set number of repeated measurements

# repeats = 2**3

# # chose the 'turtle'-method:
# # sets the light-level, measures that level repeatedly and sets the next light-level

# for i in range(2**10):
#     arduino.query(f"OUT:CH0 {i}")
#     for rep in range(repeats):

#         # measure voltages 
#         u1_adc, u2_adc= int(arduino.query("MEAS:CH1?")), int(arduino.query("MEAS:CH2?"))

#         # calculate voltages
#         u1_vol, u2_vol= C_adc_vol * u1_adc, C_adc_vol * u2_adc

#         # calculate current & voltage LED (and append to list)
#         u_LED.append(u1_vol - u2_vol)
#         I_LED.append(( u2_vol / R_ohm )* 1000)

    
#     # delete all list items except from current repeat
#     # take the average and standarddeviation using Python Standard Library module Statistics
#     # append to respective lists

#     # calculate average voltage LED and uncertainty
#     del u_LED[:-repeats]
#     u_avg.append(stats.mean(u_LED))
#     u_err.append((stats.stdev(u_LED)) / sqrt(repeats))

#     # calculate average current LED and uncertainty
#     del I_LED[:-repeats]
#     I_avg.append(stats.mean(I_LED))
#     I_err.append((stats.stdev(I_LED)) / sqrt(repeats))


# # turn LED off
# light_off = arduino.write(f"OUT:CH0 0")
# arduino.close()


# # create csv-file
# header= ['raw_value', 'u_avg (V)', 'u_err (V)', 'I_avg (mA)', 'I_err (mA)']

# # check if file already exists, sets name accordingly
# folder, n= Path("ECPC/PythonDAQ"), 1
# while (folder / f"data-{n}.csv").exists(): n+= 1
# filename= (folder / f"data-{n}.csv")

# # write information to file
# with open(filename, "w", newline="") as datafile:
#     writer= csv.writer(datafile)
#     writer.writerow(header)
#     for a, b, c, d, e in zip(range(pow(2,10)), u_avg, u_err, I_avg, I_err):
#         writer.writerow([a, b, c, d, e])
# datafile.close()

# # plot average_current_LED vs average_voltage_LED
# plt.errorbar(u_avg, I_avg, xerr= u_err, yerr= I_err, fmt=".", capsize=2,)

# plt.xlabel("LED voltage (V)")
# plt.ylabel("LED stroomsterkte (mA)")
# plt.title("I tegen U uitgezet")

# plt.grid()
# plt.show()