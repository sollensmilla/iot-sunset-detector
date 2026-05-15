# MQTT
BROKER = "broker.emqx.io"
TOPIC = b"lnu/iot/ss226uk/sensor"

# I2C
I2C_SCL = 22
I2C_SDA = 21
I2C_FREQ = 100000

# Sensor
SENSOR_ADDR = 0x44

# Registers
REG_CH0 = 0x00
REG_CH1 = 0x01
REG_CH2 = 0x02
REG_CH3 = 0x03

REG_CONFIG = 0x0A

# Data filtering
MIN_LUX_FOR_CCT = 60