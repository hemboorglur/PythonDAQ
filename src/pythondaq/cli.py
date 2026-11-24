## NOAH ZEEMAN - 15494365 - Universiteit van Amsterdam
## NSP2 - ECPC - Command-line interface "Pythondaq: veni vidi vici"
## 23 Nov '26 / 24 Nov '26 (latest change)

"""A model viewer for the command-line interface of the PythonDAQ application.
Provides methods for listing available devices, connecting to a device,
and performing diode experiments.
"""


## had problems with "WebAgg" backend on my home MacMini, so choose which one to use depending on the system.
import matplotlib
matplotlib.use("MacOSX")
# matplotlib.use("WebAgg")


import click
from pythondaq.diode_experiment import DiodeExperiment, list_resources
import csv
from pathlib import Path
import matplotlib.pyplot as plt


## hash this when not using the WebAgg backend.
# plt.rcParams["webagg.address"] = "0.0.0.0"
# plt.rcParams["webagg.port"] = 8988
# plt.rcParams["webagg.open_in_browser"] = Fals


@click.group()
def cmd_group():
    pass


@cmd_group.command()
def list():
    """List available devices.

    Returns:
        Lists the available devices that can be connected to.
    """
    return print(list_resources())


@cmd_group.command()
@click.argument(
    "port", 
    type=str, 
    help="VISA-port of the Arduino device to connect to."
)
def info(port):
    """Get the identifaction string of the connected Arduino.
    
    Args:
        port: VISA-port of the specified Arduino.
    Returns:
        Identification string of the specified Arduino
    """
    return print(DiodeExperiment(port).device.get_identification())
    
        
@cmd_group.command()
@click.option(
    "-r", "--range",
    type=tuple([float, float, int]),
    default=([0, 3.31, 1]),
    show_default=True,
    help="Scan LED with specified voltage range and repeat measurements. (minimum: 0 V, maximum: 3.31 V)"
    )
@click.option(
    "-o", "--output",
    type=str, 
    default=None,
    help="Output the measurement results to a specified CSV file."
    )
@click.option(
    "-s", "--stepsize",
    type=float,
    default=0.01,
    show_default=True,
    help="Step size (in Volt) for scanning the LED voltage range."
    )
@click.option(
    "-g/-ng", "--graph/--no-graph", 
    default=False,
    show_default=True,
    help="Plot the measurement results in a graph."
    )
@click.argument(
    "port", 
    type=str, 
    help="VISA-port of the Arduino device to connect to."
)
def scan(range, output, stepsize, graph, port):    
    
    if range[0] < 0 or range[0] > 3.31 or range[1] < 0 or range[1] > 3.31:
        return print("Voltage range must be between 0 and 3.31 V.")
    
    #device= DiodeExperiment(port="ASRL/dev/ttyACM0::INSTR")
    device = DiodeExperiment(port)
    u_avg, u_err, I_avg, I_err= device.scan(range[0], range[1], range[2], stepsize)
    print(
        f"gemiddelde spanning LED: {u_avg[-1]:.4f} +/- {u_err[-1]:.4f} V\n"
        f"gemiddelde stroomsterkte LED: {I_avg[-1]:.4f} +/- {I_err[-1]:.4f} mA" 
    )
    
    if output:
        folder= Path(__file__).resolve().parents[2] / "data-files"
        folder.mkdir(parents=True, exist_ok=True)
        filename= folder / output
        if filename.suffix != ".csv":
            filename= filename.with_suffix(".csv")

    with filename.open("w", newline="") as datafile:
        writer = csv.writer(datafile)
        writer.writerow(['raw_value', 'u_avg (V)', 'u_err (V)', 'I_avg (mA)', 'I_err (mA)'])
        writer.writerows(zip(u_avg, u_err, I_avg, I_err))
    datafile.close()
    
    if graph:
        plt.errorbar(u_avg, I_avg, xerr= u_err, yerr= I_err, fmt=".", capsize=2,)

        plt.xlabel("LED voltage (V)")
        plt.ylabel("LED stroomsterkte (mA)")
        plt.title("I tegen U uitgezet")

        plt.grid()
        plt.show()


if __name__ == "__main__":
    cmd_group()