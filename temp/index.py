# import usb.core

# dev = usb.core.find(idVendor=0x1ab1)
# print(*dev)


import pyvisa
# import matplotlib.pyplot as plt
# import RigolWFM.wfm as rigol
# # import numpy

rm = pyvisa.ResourceManager()
# rm.timeout = 20000
# print(rm.list_resources())
# scope = rm.open_resource('USB0::0x1AB1::0x04CE::DS1ZD204101021::INSTR')
print(list(filter(lambda x: 'DS1ZD204101021' in x, rm.list_resources())))
# scope = rm.open_resource('USB0::0x1AB1::0x0642::DG1ZA202603185::INSTR')
# scope.write(':STOP')

# scope.write(":WAV:MODE RAW")
# # Set return format to Byte.
# scope.write(":WAV:FORM BYTE")

# # Set waveform read start to 0.
# scope.write(":WAV:STAR 1")
# # Set waveform read stop to 250000.
# scope.write(":WAV:STOP 250000")

# Read data from the scope, excluding the first 9 bytes (TMC header).
# rawdata = scope.query_binary_values(":WAV:DATA?", datatype='B')

# print(rawdata[:100])

# # Set return format to Byte.
# inst.timeout = 25000
# inst.chunk_size = 1024000000
# result = inst.query('trace:data?')
# # result = inst.read_bytes()
# print(result)
# # print(inst.read())

# # print(result)

# # :CHANnel1:SCALe 0.5
# # :TIMebase:SCALe 0.0001

# # w = rigol.Wfm.from_file(filename, scope)
# # w.plot()
# # plt.show()

# while True:
#     inp = input('command: ')
#     result = scope.write(inp)
# print(result)

# from RsSmw import *

# Use the instr_list string items as resource names in the RsSmw constructor
# instr_list = RsSmw.list_resources("?*")
# print(instr_list)