## NOAH ZEEMAN - 15494365 - Universiteit van Amsterdam
## NSP2 - ECPC - Model-View-Controller "Pythondaq: controller afsplitsen"
## 10 Nov '26


# import necessary packages
import pyvisa

# list available Arduinos
def list_resources():
    return pyvisa.ResourceManager("@py").list_resources()


class ArduinoVISADevice:
    # constants used within the class
    C_adc_vol, C_vol_adc = 3.3/1023, 1023/3.3

    # connect to Arduino
    def __init__(self, port):
        self.arduino= pyvisa.ResourceManager("@py").open_resource(port, read_termination="\r\n", write_termination="\n")
    
    # return Arduino ID string
    def get_identification(self):
        return self.arduino.query("*IDN?")

    # set output ADC value, returns value
    def set_output_value(self, value):
        self.arduino.query(f"OUT:CH0 {value}")
        return f"{value}"

    # set output voltage, returns rounded (2 decimals) voltage
    def set_output_voltage(self, voltage):
        self.set_output_value(int(voltage * self.C_vol_adc))
        return f"{voltage:.2f} V"

    # returns current output ADC value
    def get_output_value(self):
        return self.arduino.query(f"OUT:CH0?")

    # returns current voltage
    def get_output_voltage(self):
        return f"{self.C_adc_vol * self.get_output_value():.2f}"

    # returns measured ADC value on specified channel as integer
    def get_input_value(self, channel):
        return int(self.arduino.query(f"MEAS:CH{channel}?"))

    # returns measured voltage on specified channel as rounded (2 decimals) string
    def get_input_voltage(self, channel):
        return f"{self.get_input_value(channel) * self.C_adc_vol:.2f}"