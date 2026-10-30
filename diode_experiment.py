## NOAH ZEEMAN - 15494365
## NSP2 - ECPC - basisscript voor het experiment "start script"
## 30 Oct '26

# importeren van benodigde packages
import pyvisa

# zoeken naar verbonden arduinos
rm = pyvisa.ResourceManager("@py")
ports = rm.list_resources()
print(ports)

# specifieke device aanwijzen
device = rm.open_resource(
    "ASRL/dev/ttyACM0::INSTR", read_termination="\r\n", write_termination="\n"
)

# bereik voltage 0.0 V - 3.3 V
# bereik raw_value 0 - 1023

# set output voltage from 0 to max

# constante omrekenenings-waardes:
C_raw_vol = 3.3/1023
C_vol_raw = 1023/3.3



for raw_value in range(1024):
    light = device.query(f"OUT:CH0 {raw_value}")
    voltage_LED = float(device.query("MEAS:CH0?"))
    voltage_res = float(device.query("MEAS:CH1?"))
    print(raw_value, voltage_LED)


# laatste licht-waarde uitlezen
final_value = device.query("OUT:CH0?")
print(final_value)