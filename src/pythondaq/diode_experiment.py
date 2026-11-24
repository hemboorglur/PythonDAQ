## NOAH ZEEMAN - 15494365 - Universiteit van Amsterdam
## NSP2 - ECPC - Pythonprojecten met uv "Pythondaq: veni vidi vici"
## 13 Nov '26 / 23 Nov '26 (latest change)

"""Model for performing voltage and current measurements on an LED.

Provides methods for connecting to an Arduino, scanning output voltages,
and calculating average LED voltage, current and their uncertainties.
"""

import statistics as stats
from math import sqrt
from pythondaq.arduino_device import ArduinoVISADevice, list_resources
import numpy as np


class DiodeExperiment:
    """Perform LED measurements using an ArduinoVISADevice.

    Provides methods for scanning output voltages and calculating 
    average LED voltage, current and their uncertainties.
    """

    def __init__(self, port:str) -> None:
        """Establish connection to the Arduino using ArduinoVISADevice.

            Args:
                port: VISA-address of the Arduino.
        """
        self.device= ArduinoVISADevice(port)

    def scan(self, start:int, stop:int, repeats:int) -> tuple[list[float], list[float], list[float], list[float]]:
        """Scan output voltages and measure LED voltage and current.

        Calculates the average LED voltage and current and their standard errors 
        from repeated measurements at each voltage.

        Args:
            start: Starting output voltage in volts.
            stop: Stopping output voltage in volts.
            repeats: Number of repeated measurements per voltage.

        Returns:
            Tuple with:
                u_avg: Average LED voltages in volts.
                u_err: Standard errors of average LED voltages in volts.
                I_avg: Average LED currents in milliamperes.
                I_err: Standard errors of average LED currents in milliamperes.
        """

        R_ohm = 220

        u_LED, I_LED= [], []
        u_avg, I_avg= [], []
        u_err, I_err= [], []

        for i in np.arange(start, stop, 0.01):
            self.device.set_output_voltage(i)

            for rep in range(repeats):
                u_1, u_2= float(self.device.get_input_voltage(1)), float(self.device.get_input_voltage(2))
                u_LED.append(u_1 - u_2)
                I_LED.append(u_2 / R_ohm *1000)

            del u_LED[:-repeats]
            u_avg.append(stats.mean(u_LED))

            del I_LED[:-repeats]
            I_avg.append(stats.mean(I_LED))
            
            if repeats > 1:
                u_err.append(stats.stdev(u_LED) / sqrt(repeats))
                I_err.append(stats.stdev(I_LED) / sqrt(repeats))
            else:
                u_err.append(float("nan"))
                I_err.append(float("nan"))

        self.device.set_output_voltage(0)
        return u_avg, u_err, I_avg, I_err