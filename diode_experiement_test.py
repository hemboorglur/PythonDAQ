## NOAH ZEEMAN - 15494365
## NSP2 - ECPC - basisscript voor het experiment "herhaalmetingen"
## 30 Oct '26

# importeren van benodigde packages
import pyvisa
import matplotlib
matplotlib.use("WebAgg")
import matplotlib.pyplot as plt


# instellen van een webserver waar matplotlib de grafieken kan weergeven
plt.rcParams["webagg.address"] = "192.168.2.166"
plt.rcParams["webagg.port"] = 8988
plt.rcParams["webagg.open_in_browser"] = False


# connect to Arduino
rm = pyvisa.ResourceManager("@py")
ports = rm.list_resources()
print(ports)

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

# lijsten voor de spannings- en stroomsterkte- waardes
u_LED, I_LED= [], []


# set output voltage form 0 to max
for i in range(1024):
    light_i = arduino.write(f"OUT:CH0 {i}")

    # measure voltages
    u1_adc, u2_adc= int(arduino.query("MEAS:CH1?")), int(arduino.query("MEAS:CH2?"))

    # calculate voltages
    u1_vol, u2_vol= round(C_adc_vol * u1_adc, 3), round(C_adc_vol * u2_adc, 3)

    # calculate current & voltage LED (and append to list)
    u_LED.append(round(u1_vol - u2_vol, 3))
    I_LED.append(round(( u2_vol / R_ohm )* 1000, 3))

    # print voltage: voltage_LED V (raw_voltage_LED) current: current_LED A
    print(
        f"ruwe waarde spanning LED: {u1_adc - u2_adc} ({u_LED[-1]} V)\n"
        f"ruwe waarde spanning weerstand: {u2_adc} ({u2_vol} V)\n"
        f"stroomsterkte LED: {I_LED[-1]} mA"
    )


# turn LED off
light_off = arduino.write(f"OUT:CH0 0")
arduino.close()


# plot current_LED vs voltage_LED
plt.scatter(u_LED, I_LED, s=8)

plt.xlabel("LED voltage (V)")
plt.ylabel("LED stroomsterkte (mA)")
plt.title("I tegen U uitgezet")

plt.grid()
plt.show()