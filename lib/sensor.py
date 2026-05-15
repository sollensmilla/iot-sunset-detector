import time

from machine import I2C, Pin

from config import (
    I2C_SCL,
    I2C_SDA,
    I2C_FREQ,

    SENSOR_ADDR,

    REG_CH0,
    REG_CH1,
    REG_CH2,
    REG_CH3,

    REG_CONFIG
)

class ColorSensor:

    def __init__(self):

        self.i2c = I2C(
            0,
            scl=Pin(I2C_SCL),
            sda=Pin(I2C_SDA),
            freq=I2C_FREQ
        )

        self.addr = SENSOR_ADDR

        print("I2C scan:", self.i2c.scan())

        self.configure()

    def configure(self):

        try:

            config = bytes([0x32, 0x30])

            self.i2c.writeto_mem(
                self.addr,
                REG_CONFIG,
                config
            )

            print("Sensor configured")

        except Exception as e:

            print("Sensor init error:", e)

        time.sleep(2)

    def read_channel_raw(self, register):

        data = self.i2c.readfrom_mem(
            self.addr,
            register,
            3
        )

        b0 = data[0]
        b1 = data[1]
        b2 = data[2]

        exponent = (b0 >> 4) & 0x0F

        mantissa = (
            ((b0 & 0x0F) << 16)
            | (b1 << 8)
            | b2
        )

        raw = mantissa * (2 ** exponent)

        return raw

    def read_lux(self):

        ch0 = self.read_channel_raw(REG_CH0)

        lux = round(ch0 * 0.00215, 2)

        return lux

    def read_rgb_raw(self):

        red_raw = self.read_channel_raw(REG_CH1)

        green_raw = self.read_channel_raw(REG_CH2)

        blue_raw = self.read_channel_raw(REG_CH3)

        return (
            red_raw,
            green_raw,
            blue_raw
        )