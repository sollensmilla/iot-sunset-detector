from machine import Pin, I2C
import time

print("Starting in 5 seconds...")
time.sleep(5)

i2c = I2C(0, scl=Pin(22), sda=Pin(21))

ADDR = 0x44

# Konfigurationsvärde
config = bytes([0x12, 0x34])

# Skriv till config-register
i2c.writeto_mem(ADDR, 0x0A, config)

time.sleep(1)

while True:
    try:
        # Läs från channel/register
        data = i2c.readfrom_mem(ADDR, 0x00, 2)

        value = (data[0] << 8) | data[1]

        print("Raw:", value)

    except Exception as e:
        print("Error:", e)

    time.sleep(2)