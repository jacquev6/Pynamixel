# coding: utf8

# Copyright 2015 Vincent Jacques <vincent@vincent-jacques.net>

import unittest

import MockMockMock


def compute_checksum(payload):
    return ~(sum(payload)) & 0xFF


class CommunicationError(Exception):
    pass


class Bus(object):
    def __init__(self, hardware):
        self.__hardware = hardware

    def send(self, ident, instruction, parameters):
        self.__send(ident, instruction, parameters)
        return self.__receive()

    def broadcast(self, instruction, parameters):
        self.__send(0xFE, instruction, parameters)

    def __send(self, ident, instruction, parameters):
        length = len(parameters) + 2
        payload = [ident, length, instruction] + parameters
        checksum = compute_checksum(payload)
        packet = [0xFF, 0xFF] + payload + [checksum]
        self.__hardware.send(packet)

    def __receive(self):
        # @todo Catch and translate exceptions raised by hardware
        ff1, ff2, ident, length = self.__receive_from_hardware(4)
        if ff1 != 0xFF or ff2 != 0xFF:
            raise CommunicationError
        payload = self.__receive_from_hardware(length)
        error = payload[0]
        parameters = payload[1:-1]
        checksum = payload[-1]
        payload = [ident, length, error] + parameters
        if checksum != compute_checksum(payload):
            raise CommunicationError
        return ident, error, parameters

    def __receive_from_hardware(self, count):
        payload = self.__hardware.receive(count)
        if len(payload) != count:
            raise CommunicationError
        return payload


class ComputeChecksumTestCase(unittest.TestCase):
    def test(self):
        # From http://support.robotis.com/en/product/dynamixel/communication/dxl_packet.htm
        self.assertEqual(compute_checksum([0x01, 0x05, 0x03, 0x0C, 0x64, 0xAA]), 0xDC)


class BusTestCase(unittest.TestCase):
    def setUp(self):
        super(BusTestCase, self).setUp()
        self.mocks = MockMockMock.Engine()
        self.hardware = self.mocks.create("hardware")
        self.bus = Bus(self.hardware.object)

    def tearDown(self):
        self.mocks.tearDown()
        super(BusTestCase, self).tearDown()

    def test_send(self):
        # From http://support.robotis.com/en/product/dynamixel/communication/dxl_instruction.htm (example 1)
        self.hardware.expect.send([0xFF, 0xFF, 0x01, 0x04, 0x02, 0x2B, 0x01, 0xCC])
        self.hardware.expect.receive(4).andReturn([0xFF, 0xFF, 0x01, 0x03])
        self.hardware.expect.receive(3).andReturn([0x00, 0x20, 0xDB])
        ident, error, parameters = self.bus.send(0x01, 0x02, [0x2B, 0x01])
        self.assertEqual(ident, 0x01)
        self.assertEqual(error, 0x00)
        self.assertEqual(parameters, [0x20])

    def test_broadcast(self):
        # From http://support.robotis.com/en/product/dynamixel/communication/dxl_instruction.htm (example 2)
        self.hardware.expect.send([0xFF, 0xFF, 0xFE, 0x04, 0x03, 0x03, 0x01, 0xF6])
        self.bus.broadcast(0x03, [0x03, 0x01])

    def test_hardware_returns_wrong_number_of_bytes(self):
        self.hardware.expect.send([0xFF, 0xFF, 0x01, 0x04, 0x02, 0x2B, 0x01, 0xCC])
        self.hardware.expect.receive(4).andReturn([0xFF, 0xFF, 0x01])
        with self.assertRaises(CommunicationError):
            self.bus.send(0x01, 0x02, [0x2B, 0x01])

    def test_hardware_returns_not_ffff(self):
        self.hardware.expect.send([0xFF, 0xFF, 0x01, 0x04, 0x02, 0x2B, 0x01, 0xCC])
        self.hardware.expect.receive(4).andReturn([0xFE, 0xFF, 0x01, 0x00])
        with self.assertRaises(CommunicationError):
            self.bus.send(0x01, 0x02, [0x2B, 0x01])

    def test_wrong_checksum(self):
        self.hardware.expect.send([0xFF, 0xFF, 0x01, 0x04, 0x02, 0x2B, 0x01, 0xCC])
        self.hardware.expect.receive(4).andReturn([0xFF, 0xFF, 0x01, 0x03])
        self.hardware.expect.receive(3).andReturn([0x00, 0x20, 0xDA])
        with self.assertRaises(CommunicationError):
            self.bus.send(0x01, 0x02, [0x2B, 0x01])