# !/usr/bin/python
import smbus
import math

# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

bus = smbus.SMBus(1)
address = 0x68
bus.write_byte_data(address, power_mgmt_1, 0)


def read_byte(reg):
    return bus.read_byte_data(address, reg)


def read_word(reg):
    h = bus.read_byte_data(address, reg)
    r_data = bus.read_byte_data(address, reg + 1)
    value = (h << 8) + r_data
    return value


def read_word_2c(reg):
    val = read_word(reg)
    if val >= 0x8000:
        return -((65535 - val) + 1)
    else:
        return val


def dist(a, b):
    return math.sqrt((a * a) + (b * b))


def get_y_rotation(x, y, z):
    radians = math.atan2(x, dist(y, z))
    return -math.degrees(radians)


def get_x_rotation(x, y, z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)


def get_all_gyro_data():
    acceleration_xout = read_word_2c(0x3b)
    acceleration_yout = read_word_2c(0x3d)
    acceleration_zout = read_word_2c(0x3f)

    acceleration_xout_scaled = round(acceleration_xout / 16384.0, 3)
    acceleration_yout_scaled = round(acceleration_yout / 16384.0, 3)
    acceleration_zout_scaled = round(acceleration_zout / 16384.0, 3)

    x_rotation = round(
        get_x_rotation(acceleration_xout_scaled, acceleration_yout_scaled, acceleration_zout_scaled), 0)
    y_rotation = round(
        get_y_rotation(acceleration_xout_scaled, acceleration_yout_scaled, acceleration_zout_scaled), 0)

    return {'acc': [acceleration_xout, acceleration_yout, acceleration_zout],
            'acc_sca': [acceleration_xout_scaled, acceleration_yout_scaled, acceleration_zout_scaled],
            'rot': [x_rotation, y_rotation]}
