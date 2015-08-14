# coding: utf8

# Copyright 2015 Vincent Jacques <vincent@vincent-jacques.net>

import unittest

from .fields import RW8, RW16, R8, R16


class AXS1(object):
    def __init__(self, bus, ident):
        self.__bus = bus
        self.__ident = ident
        # http://support.robotis.com/en/product/auxdevice/sensor/dxl_ax_s1.htm#Ax_S1_Address_26
        # EEPROM area
        self.model_number = R16(bus, ident, 0x00)
        self.firmware_version = R8(bus, ident, 0x02)
        self.ident = RW8(bus, ident, 0x03)
        self.baud_rate = RW8(bus, ident, 0x04)
        self.return_delay_time = RW8(bus, ident, 0x05)
        self.status_return_level = RW8(bus, ident, 0x10)
        # RAM area
        self.ir_left_fire_data = R8(bus, ident, 0x1A)
        self.ir_center_fire_data = R8(bus, ident, 0x1B)
        self.ir_right_fire_data = R8(bus, ident, 0x1C)
        self.light_left_data = R8(bus, ident, 0x1D)
        self.light_center_data = R8(bus, ident, 0x1E)
        self.light_right_data = R8(bus, ident, 0x1F)
        self.ir_obstacle_detected = R8(bus, ident, 0x20)
        self.light_detected = R8(bus, ident, 0x21)
        self.sound_data = R8(bus, ident, 0x23)
        self.sound_data_max_hold = RW8(bus, ident, 0x24)
        self.sound_detected_count = RW8(bus, ident, 0x25)
        self.sound_detected_time = RW16(bus, ident, 0x26)
        self.buzzer_note = RW8(bus, ident, 0x28)
        self.buzzer_ringing_time = RW8(bus, ident, 0x29)
        self.registered = RW8(bus, ident, 0x2C)
        self.ir_remocon_arrived = R8(bus, ident, 0x2E)
        self.lock = RW8(bus, ident, 0x2F)
        self.remocon_rx = R16(bus, ident, 0x30)
        self.remocon_tx = RW16(bus, ident, 0x32)
        self.ir_obstacle_detect_compare_rd = RW8(bus, ident, 0x34)
        self.light_detect_compare_rd = RW8(bus, ident, 0x35)


class AXS1TestCase(unittest.TestCase):
    pass