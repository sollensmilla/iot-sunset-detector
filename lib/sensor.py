from machine import I2C, Pin

class ColorSensor:

    def __init__(self):
        self.i2c = I2C(
            0,
            scl=Pin(22),
            sda=Pin(21)
        )

        self.addr = 0x44

        self.configure()

    def configure(self):
        config = bytes([0x32, 0x30])

        self.i2c.writeto_mem(
            self.addr,
            0x0A,
            config
        )

    def read_channel(self, register):
        ...