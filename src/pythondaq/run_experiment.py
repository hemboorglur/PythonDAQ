## NOAH ZEEMAN - 15494365 - Universiteit van Amsterdam
## NSP2 - ECPC - Pythonprojecten met uv "Pythondaq: veni vidi vici"
## 13 Nov '26 / 23 Nov '26 (latest change)

"""Run the LED experiment and display the measurement results.

Uses DiodeExperiment to measure LED voltage and current, saves
the results to a CSV file, and plots the current-voltage characteristic
with error bars.
"""

from pythondaq.diode_experiment import DiodeExperiment, list_resources
import csv
from pathlib import Path

# choose the backend for matplotlib depending on the system
import matplotlib
# matplotlib.use("WebAgg")
matplotlib.use("MacOSX")

# don't hash this line
import matplotlib.pyplot as plt

# set webserver for rendering
# plt.rcParams["webagg.address"] = "0.0.0.0"
# plt.rcParams["webagg.port"] = 8988
# plt.rcParams["webagg.open_in_browser"] = False


def run(start:float, stop:float, repeat:int, stepsize:float) -> None:
    """Run an LED voltage scan and process the measurement results.

    Connects to the Arduino, performs repeated measurements, saves
    the results to a CSV file - without overriding previous measurements-,
    and plots the LED current-voltage with error bars.

    Args:
        start: Starting output voltage in volts.
        stop: Stopping output voltage in volts.
        repeat: Number of repeated measurements.
        stepsize: Size of the voltage steps in volts.
       """

    print(list_resources())
    
    device= DiodeExperiment(port="ASRL/dev/ttyACM0::INSTR")
    u_avg, u_err, I_avg, I_err= device.scan(start, stop, repeat, stepsize)
    print(
        f"gemiddelde spanning LED: {u_avg[-1]:.4f} +/- {u_err[-1]:.4f} V\n"
        f"gemiddelde stroomsterkte LED: {I_avg[-1]:.4f} +/- {I_err[-1]:.4f} mA" 
    )


    folder, n= Path(__file__).resolve().parents[2] / "data_files", 1
    while (folder / f"data-{n}.csv").exists(): n+= 1
    filename= (folder / f"data-{n}.csv")

    with filename.open("w", newline="") as datafile:
        writer = csv.writer(datafile)
        writer.writerow(['raw_value', 'u_avg (V)', 'u_err (V)', 'I_avg (mA)', 'I_err (mA)'])
        writer.writerows(zip(u_avg, u_err, I_avg, I_err))
    datafile.close()

    plt.errorbar(u_avg, I_avg, xerr= u_err, yerr= I_err, fmt=".", capsize=2,)

    plt.xlabel("LED voltage (V)")
    plt.ylabel("LED stroomsterkte (mA)")
    plt.title("I tegen U uitgezet")

    plt.grid()
    plt.show()
    
run(0, 3.31, 1, 0.01)