from pymodbus.client.sync import ModbusTcpClient as ModbusClient

cli = ModbusClient('localhost', port=5020)
assert cli.connect()
res = cli.read_holding_registers(0x00, count=2, unit=1)
assert not res.isError()
print(res.registers)