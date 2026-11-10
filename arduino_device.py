## NOAH ZEEMAN - 15494365 - Universiteit van Amsterdam
## NSP2 - ECPC - Model-View-Controller "Pythondaq: controller afsplitsen"
## 10 Nov '26


# import necessary packages
import pyvisa

# list available Ardiunos
def list_resources():
    return pyvisa.ResourceManager("@py").list_resources()


class ArduinoVISADevice:
    # constants used within the class
    C_adc_vol, C_vol_adc = 3.3/1023, 1023/3.3

    def __init__(self, port):
        self.arduino= pyvisa.ResourceManager("@py").open_resource(port, read_termination="\r\n", write_termination="\n")
    
    def get_identification(self):
        return self.arduino.query("*IDN?")

    def set_output_value(self, value):
        self.arduino.query(f"OUT:CH0 {value}")
        return f"{value}"

    def set_output_voltage(self, voltage):
        self.set_output_value(int(voltage * self.C_vol_adc))
        return f"{voltage:.2f} V"

    def get_output_value(self):
        return self.arduino.query(f"OUT:CH0?")

    def get_output_voltage(self, channel):
        return f"{self.C_adc_vol * self.get_output_value():.2f}"

    def get_input_value(self, channel):
        return int(self.arduino.query(f"MEAS:CH{channel}?"))

    def get_input_voltage(self, channel):
        return f"{self.get_input_value(channel) * self.C_adc_vol:.2f}"

    