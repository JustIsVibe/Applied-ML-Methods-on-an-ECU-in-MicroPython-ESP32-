from machine import ADC, Pin
class AdcSensor:
    def __init__(self, pin=34, atten=ADC.ATTN_11DB):
        self.adc=ADC(Pin(pin)); self.adc.atten(atten)
    def read_raw(self): return self.adc.read()
