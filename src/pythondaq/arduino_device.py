## NOAH ZEEMAN - 15494365 - Universiteit van Amsterdam
## NSP2 - ECPC - Pythonprojecten met uv "Pythondaq: applicatie"
## 13 Nov '26

"""Controller for communicating with an Arduino through PyVISA.

Provides methods for connecting to the Arduino, controlling its
output channel, and reading voltage measurements from input channels.
"""

import pyvisa

def list_resources() -> list[str]:
    """List all available Arduino's
    
    Returns: 
        a list of the ports of all available Arduino's
    """
    return pyvisa.ResourceManager("@py").list_resources()


class ArduinoVISADevice:
    """Control the Arduino device using the VISA communication protocol.

    Provides methods for setting output values and reading
    measurements from the Arduino's input channels.
    """    

    def __init__(self, port: str) -> None:
        """Establish connection to specified Arduino and set class constants

        Args: 
            port: VISA-address of the Arduino.
        """
        self.arduino= pyvisa.ResourceManager("@py").open_resource(port, read_termination="\r\n", write_termination="\n")
        self.C_adc_vol, self.C_vol_adc = 3.3/1023, 1023/3.3
    
    def get_identification(self) -> str:
        """Get Arduino identification string

        Returns: 
            Arduino identification string
        """
        return self.arduino.query("*IDN?")

    def set_output_value(self, value:int) -> int:
        """Set ADC value on output channel 0

        Args: 
            value: integer ADC value to put on output channel 0
        """
        ## return self.arduino.query(f"OUT:CH0 {value}")

        self.arduino.query(f"OUT:CH0 {value}")

    def set_output_voltage(self, voltage: int) -> str:
        """Set the voltage on Arduino output channel 0

        Converts the voltage to an ADC value using ADC conversion factor
            
        Returns: 
            Measured voltage in volts - formatted to two decimal places - as a string.
        """

        self.set_output_value(int(voltage * self.C_vol_adc))
        return f"{voltage:.2f} V"


    def get_output_value(self) -> str:
        """Measures current ADC value on output channel 0

        Returns:
            Measured ADC value on output channel 0 as a string
        """
        return self.arduino.query(f"OUT:CH0?")

    def get_output_voltage(self) -> str:
        """Measures current voltage on output channel 0

        Converts the ADC value to voltage using ADC conversion factor

        Returns:
            Measured voltage in volts - formatted to two decimal places - as a string.
        """
        return f"{self.C_adc_vol * self.get_output_value():.2f}"

    def get_input_value(self, channel: int) -> int:
        """Measure ADC level on specified input channel
        
        Args:
            channel: input channel number to measure
        Returns:
            Measured ADC value
        """
        return int(self.arduino.query(f"MEAS:CH{channel}?"))

    def get_input_voltage(self, channel: int) -> str:
        """Measure voltage on specified input channel formatted to two decimal places

        Converts the ADC value to voltage using ADC conversion factor 

        Args:
            channel: input channel number to measure
        Returns:
            Measured voltage in volt - formatted to two decimal places - as a string
        """
        return f"{self.get_input_value(channel) * self.C_adc_vol:.2f}"