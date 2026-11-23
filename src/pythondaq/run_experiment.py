## NOAH ZEEMAN - 15494365
## NSP2 - ECPC - Pythonprojecten met uv "Pythondaq: applicatie"
## 13 Nov '26 / 23 Nov '26 (latest change)

"""Run the LED experiment and display the measurement results.

Uses DiodeExperiment to measure LED voltage and current, saves
the results to a CSV file, and plots the current-voltage characteristic
with error bars.
"""

from pythondaq.diode_experiment import DiodeExperiment, list_resources
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


def run(start:int, stop:int, repeat:int) -> None:
    """Run an LED voltage scan and process the measurement results.

    Connects to the Arduino, performs repeated measurements, saves
    the results to a CSV file - without overriding previous measurements-,
    and plots the LED current-voltage with error bars.

    Args:
        start: Starting output voltage in volts.
        stop: Stopping output voltage in volts.
        repeat: Number of repeated measurements.
       """

    print(list_resources())
    
    device= DiodeExperiment(port="ASRL/dev/ttyACM0::INSTR")
    u_avg, u_err, I_avg, I_err= device.scan(start, stop, repeat)
    print(
        f"gemiddelde spanning LED: {u_avg[-1]:.4f} +/- {u_err[-1]:.4f} V\n"
        f"gemiddelde stroomsterkte LED: {I_avg[-1]:.4f} +/- {I_err[-1]:.4f} mA" 
    )

    header= ['raw_value', 'u_avg (V)', 'u_err (V)', 'I_avg (mA)', 'I_err (mA)']

    folder, n= Path(__file__).resolve().parents[2] / "data_files", 1
    while (folder / f"data-{n}.csv").exists(): n+= 1
    filename= (folder / f"data-{n}.csv")

    with open(filename, "w", newline="") as datafile:
        writer= csv.writer(datafile)
        writer.writerow(header)
        for a, b, c, d, e in zip(range(pow(2,10)), u_avg, u_err, I_avg, I_err):
            writer.writerow([a, b, c, d, e])
    datafile.close()

    plt.errorbar(u_avg, I_avg, xerr= u_err, yerr= I_err, fmt=".", capsize=2,)

    plt.xlabel("LED voltage (V)")
    plt.ylabel("LED stroomsterkte (mA)")
    plt.title("I tegen U uitgezet")

    plt.grid()
    plt.show()