 # -*- coding: utf-8 -*-
"""
wraps calling the D4100 driver api dlls into a set of object oriented interfaces.

author: Danyal Ahsanullah
"""
# __author__ = 'Danyal Ahsanullah'
__ver_info = (0,0,0)
__version__ = '.'.join(map(str, __ver_info))


import typing as _typ
import ctypes as _ctypes
from collections import namedtuple as _namedtuple
from dataclasses import dataclass as _dataclass 
from enum import Enum as _Enum
from os import ( getcwd as _getcwd, chdir as _chdir )
from atexit import ( register as _register, unregister as _unregister )



# load DLL

# check what bit version python
from struct import calcsize as _calcsize
if _calcsize('P')*8 == 64:
    from client64 import D4100_DLL as _dmd_dll
else:
    raise NotImplementedError('native 32-bit support has not been implemented yet')
    from ctypes import cdll
    _dmd_dll = cdll('../lib/D4100_usb.dll')
# encourage gc to remove _calcsize
del _calcsize # removes namespace entry
# del sys.modules['_calcsize']

class DMDType(Enum):
    DLP9500 = 0
    DLP7000 = 1
    DLP650LNIR = 7
    NA = 15

_DMD = _namedtuple('DMD','rows cols dmd_type')

class DMD(_DMD):
    pass


DLP9500 = DMD(rows=1080,cols=1920,dmd_type=DMDType.DLP9500)
DLP7000 = DMD(rows=768,cols=1024,dmd_type=DMDType.DLP7000) 
DLP650LNIR = DMD(rows=800,cols=1280,dmd_type=DMDType.DLP650LNIR)
BAD_DMD = DMD(rows=0,cols=0, DMDType.NA)

DMD_MAP = {
    0:DLP9500,
    1:DLP7000,
    7:DLP650LNIR,
    15:BAD_DMD,
}



# # util funcs
def load_dll(base_path, dll_name):
    cwd = _getcwd()
    _chdir(basepath)  
    dll = _ctypes.cdll.LoadLibrary(dll_name)
    _chdir(cwd)
    return dll


class D4100:
    def __init__(self):
        self._lib = None
        self.dmd = BAD_DMD

    @property
    def all_on_pattern(self):
        return bytearray([0xff]*self.dmd.rows*(self.dmd.cols//8))

    @property
    def all_off_pattern(self):
        return bytearray([0x00]*self.dmd.rows*(self.dmd.cols//8))


    def float_mirrors(self):

#     @classmethod
#     def get_controller(cls, idx=None,):
#         if not _initialized:
#             num_devices = D4100_dll.GetNumDev()
#             # build controller map
#             for i in range(0,num_devices):
#                 handle = _MightexDLL.MTUSB_LEDDriverOpenDevice(i)
#                 # send command if needed:
#                 # _MightexDLL.MTUSB_LEDDriverSendCommand(handle, c_char_p('ECHOOFF\n\r'.encode(_ENCODING)))
#                 buf = _ctypes.create_string_buffer(SERIAL_NUMBER_SIZE)
#                 _MightexDLL.MTUSB_LEDDriverSerialNumber(handle, buf,SERIAL_NUMBER_SIZE)
#                 _controller_map[i] = buf.value.decode(_ENCODING)
#                 _MightexDLL.MTUSB_LEDDriverCloseDevice(handle)


    # def __init__(self, idx):
    #     self._handle = 
