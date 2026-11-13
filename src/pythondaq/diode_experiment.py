## NOAH ZEEMAN - 15494365
## NSP2 - ECPC - Model-View-Controller "Pythondaq: model en view afsplitsen"
## 10 Nov '26


# import necessary packages
import statistics as stats
from math import sqrt
from pythondaq.arduino_device import ArduinoVISADevice, list_resources
import numpy as np


class DiodeExperiment:
    # connect to Arduino via class ArduinoVISADevice
    def __init__(self, port):
        self.device= ArduinoVISADevice(port)

    # run scan with start, stop and repeat parameters
    def scan(self, start, stop, repeats):

        # define constants and lists
        R_ohm = 220

        u_LED, I_LED= [], []
        u_avg, I_avg= [], []
        u_err, I_err= [], []

        # set output voltage from start to stop
        for i in np.arange(start, stop, 0.01):
            self.device.set_output_voltage(i)
            # print(self.device.set_output_voltage(i))

            # set number of repeated measurements
            for rep in range(repeats):

                # measure voltages
                u_1, u_2= float(self.device.get_input_voltage(1)), float(self.device.get_input_voltage(2))
                
                # calculate voltage LED
                u_LED.append(u_1 - u_2)

                # calculate current LED
                I_LED.append(u_2 / R_ohm *1000)

            # calculate average voltage LED and uncertainty
            del u_LED[:-repeats]
            u_avg.append(stats.mean(u_LED))
            u_err.append((stats.stdev(u_LED)) / sqrt(repeats))

            # calculate average current LED and uncertainty
            del I_LED[:-repeats]
            I_avg.append(stats.mean(I_LED))
            I_err.append((stats.stdev(I_LED)) / sqrt(repeats))

        # turn LED off
        self.device.set_output_voltage(0)

        # return average voltage LED, average current LED, error average voltage LED and error average current LED
        return u_avg, u_err, I_avg, I_err