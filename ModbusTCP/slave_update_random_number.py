from pymodbus.server.asynchronous import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer, ModbusAsciiFramer
from twisted.internet.task import LoopingCall
from threading import Thread
import pid
import threading
from time import sleep
from random import randrange
import os
import random


class Temp(Thread):
    def __init__(self):
        Thread.__init__(self)
        super(Temp, self).__init__()
        self._stop = threading.Event()
        self.currentTemp = 0
        self.currentHum = 0
        self.enabled = True
        self.Run = True

    def run(self):
        sleep(.5)

    # returns the current temp for the probe
    def getCurrentTemp(self):
        return random.randint(1,10)
        # return self.currentTemp

    def getCurrentHum(self):
        return random.randint(1,10)
        # return self.currentHum

    # setter to enable this probe
    def setEnabled(self, enabled):
        self.enabled = enabled

    # getter
    def isEnabled(self):
        return self.enabled


def updating_writer(a):
    context = a[0]
    function_code = 3
    slave_id = 0x00
    address = 0x00
    global temp
    # uncomment to debug temperature
    values = context[slave_id].getValues(function_code, address, count=2)
    print "prevTemp: ", values[0], " // prevHum: ", values[1]
    values = [temp.getCurrentTemp(), temp.getCurrentHum()]
    context[slave_id].setValues(function_code, address, values)
    values = context[slave_id].getValues(function_code, address, count=2)
    print "nextTemp: ", values[0], " // nextHum: ", values[1]


def main():
    store = ModbusSlaveContext(di=ModbusSequentialDataBlock(0, [10, 5]),)
    context = ModbusServerContext(slaves=store, single=True)
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/simplyautomationized'
    identity.ProductName = 'pymodbus Server'
    identity.ModelName = 'pymodbus Server'
    identity.MajorMinorRevision = '1.0'

    loop = LoopingCall(updating_writer, a=(context,))
    loop.start(.5)  # initially delay by time
    StartTcpServer(context, identity=identity, address=("localhost", 5020))
    # cleanup async tasks
    temp.setEnabled(False)
    loop.stop()


if __name__ == "__main__":
    temp = Temp()
    temp.start()
    main()