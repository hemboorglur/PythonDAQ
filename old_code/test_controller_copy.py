## NOAH ZEEMAN - 15494365 - Universiteit van Amsterdam
## NSP2 - ECPC - Model-View-Controller "Pythondaq: controller bouwen"
## 6 Nov '26


# import necessary packages
import pyvisa


# list available Ardiunos
def list_resources():
    return pyvisa.ResourceManager("@py").list_resources()


class ArduinoVISADevice:
    # constants used within the class
    C_adc_vol, C_vol_adc = 3.3/1023, 1023/3.3

    def __init__(self, port):
        self.arduino= pyvisa.ResourceManager("@py").open_resource("ASRL/dev/ttyACM0::INSTR", read_termination="\r\n", write_termination="\n")
    
    def get_identification(self):
        return self.arduino.query("*IDN?")

    def set_output_value(self, value):
        self.arduino.write(f"OUT:CH0 {value}")
        return f"{value}"

    def set_output_voltage(self, voltage):
        self.set_output_value(int(voltage * self.C_vol_adc))
        return f"{voltage} V"

    def get_output_value(self):
        return self.arduino.query(f"OUT:CH0?")

    def get_output_voltage(self, channel):
        return f"{self.C_adc_vol * self.get_output_value():.2f}"

    def get_input_value(self, channel):
        return int(self.arduino.query(f"MEAS:CH{channel}?"))

    def get_input_voltage(self, channel):
        return f"{self.get_input_value(channel) * self.C_adc_vol:.2f} V"

    

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

ch1_value = device.get_input_value(channel=1)
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