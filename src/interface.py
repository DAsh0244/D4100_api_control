 # -*- coding: utf-8 -*-
"""
wraps calling the D4100 driver api dlls into a set of object oriented interfaces.

author: Danyal Ahsanullah
"""
# __author__ = 'Danyal Ahsanullah'
__ver_info = (0,0,0)
__version__ = '.'.join(map(str, __ver_info))


# import typing as _typ
# import ctypes as _ctypes
# from enum import Enum as _Enum
# from os import ( getcwd as _getcwd, chdir as _chdir )
# from atexit import ( register as _register, unregister as _unregister )


# # DLL info
# # CONSIDER: making this an env var?
# __x64_BASE_PATH = '../lib/'
# __x86_BASE_PATH = '../lib/'
# __cdecl_dll = 'D4100_usb.dll'
# __stddel_dll = 'D4100_usb.dll'
# # MightexDLL = CDLL('../mightex_lib/x64_lib/Mightex_LEDDriver_SDK.dll')

# # util funcs
# def _get_dll(base_path:str, dll_type:str) -> _typ.Union[_ctypes.CDLL,_ctypes.WinDLL]:
#     """
#     Loads the desired dll and returns the loaded DLL object.
    
#     Arguments:
#         base_path {str} -- Path to the directory that contains the DLL
#         dll_type {str} -- DLL filename
    
#     Returns:
#         CDLL or WinDLL -- Loaded Mightex CDLL object
#     """
#     cwd = _getcwd()
#     _chdir(base_path)
#     if 'stdcall' in dll_type.lower():
#         dll_class = _ctypes.windll
#     else:
#         dll_class = _ctypes.cdll
#     dll = dll_class.LoadLibrary(dll_type)
#     _chdir(cwd)
#     return dll


# D4100_dll = _get_dll(__x64_BASE_PATH,__cdecl_dll)

# api listing:
# int program_FPGA(UCHAR* write_buffer, long write_size, short int DeviceNumber)
# short GetNumDev( )
# int GetDescriptor(int*, short DeviceNum)
# unsigned int GetDriverRev(short DeviceNumber)
# unsigned int GetFirmwareRev(short DeviceNumber)
# short int GetUsbSpeed(short DeviceNumber)
# unsigned int GetDLLRev( )
# unsigned int GetFPGARev(short DeviceNumber)
# short GetDDCVERSION(short DeviceNumber)
# short GetDMDTYPE(short DeviceNumber)
# short LoadControl(short DeviceNumber)
# int LoadData(UCHAR* RowData, unsigned int length, short DMDType, short DeviceNumber)
# short ClearFifos(short DeviceNumber)
# short SetBlkMd(short value, short DeviceNumber)
# short GetBlkMd(short DeviceNumber)
# short SetBlkAd(short value, short DeviceNumber)
# short GetBlkAd(short DeviceNumber)
# short SetRST2BLKZ(short value, short DeviceNumber)
# short GetRST2BLKZ(short DeviceNumber)
# short SetRowMd(short value, short DeviceNumber)
# short GetRowMd(short DeviceNumber)
# short SetRowAddr(short value, short DeviceNumber)
# short GetRowAddr(short DeviceNumber)
# short SetCOMPDATA(short value, short DeviceNumber)
# short GetCOMPDATA(short DeviceNumber)
# short SetNSFLIP(short value, short DeviceNumber)
# short GetNSFLIP(short DeviceNumber)
# short SetWDT(short value, short DeviceNumber)
# short GetWDT(short DeviceNumber)
# short SetPWRFLOAT(short value, short DeviceNumber)
# short GetPWRFLOAT(short DeviceNumber)
# short SetEXTRESETENBL(short value, short DeviceNumber)
# short GetEXTRESETENBL(short DeviceNumber)
# short SetGPIO(short value, short DeviceNumber)
# short GetGPIO(short DeviceNumber)
# short GetRESETCOMPLETE(int waittime, short int DeviceNumber)
# short SetGPIORESETCOMPLETE(short DeviceNumber)
# short GetSWOverrideEnable(short DeviceNumber)
# short SetSWOverrideEnable(short value, short DeviceNumber)
# short GetSWOverrideValue(short DeviceNumber)
# short SetSWOverrideValue(short value, short DeviceNumber)
# short GetTPGEnable(short DeviceNumber)
# short SetTPGEnable(short value, short DeviceNumber)
# short GetPatternForce(short DeviceNumber)
# short SetPatternForce(short value, short DeviceNumber)
# short GetPatternSelect(short DeviceNumber)
# short SetPatternSelect(short value, short DeviceNumber)
# short GetLoad4(short DeviceNumber)
# short SetLoad4(short value, short DeviceNumber)

# program_FPGA(UCHAR* write_buffer, long write_size, short int DeviceNumber)
# GetDescriptor(int*, short DeviceNum)
# GetDriverRev(short DeviceNumber)
# GetFirmwareRev(short DeviceNumber)
# GetUsbSpeed(short DeviceNumber)
# GetDLLRev()
# GetFPGARev(short DeviceNumber)
# GetDDCVERSION(short DeviceNumber)
# GetDMDTYPE(short DeviceNumber)
# LoadControl(short DeviceNumber)
# LoadData(UCHAR* RowData, unsigned int length, short DMDType, short DeviceNumber)
# ClearFifos(short DeviceNumber)
# SetBlkMd(short value, short DeviceNumber)
# GetBlkMd(short DeviceNumber)
# SetBlkAd(short value, short DeviceNumber)
# GetBlkAd(short DeviceNumber)
# SetRST2BLKZ(short value, short DeviceNumber)
# GetRST2BLKZ(short DeviceNumber)
# SetRowMd(short value, short DeviceNumber)
# GetRowMd(short DeviceNumber)
# SetRowAddr(short value, short DeviceNumber)
# GetRowAddr(short DeviceNumber)
# SetCOMPDATA(short value, short DeviceNumber)
# GetCOMPDATA(short DeviceNumber)
# SetNSFLIP(short value, short DeviceNumber)
# GetNSFLIP(short DeviceNumber)
# SetWDT(short value, short DeviceNumber)
# GetWDT(short DeviceNumber)
# SetPWRFLOAT(short value, short DeviceNumber)
# GetPWRFLOAT(short DeviceNumber)
# SetEXTRESETENBL(short value, short DeviceNumber)
# GetEXTRESETENBL(short DeviceNumber)
# SetGPIO(short value, short DeviceNumber)
# GetGPIO(short DeviceNumber)
# GetRESETCOMPLETE(int waittime, short int DeviceNumber)
# SetGPIORESETCOMPLETE(short DeviceNumber)
# GetSWOverrideEnable(short DeviceNumber)
# SetSWOverrideEnable(short value, short DeviceNumber)
# GetSWOverrideValue(short DeviceNumber)
# SetSWOverrideValue(short value, short DeviceNumber)
# GetTPGEnable(short DeviceNumber)
# SetTPGEnable(short value, short DeviceNumber)
# GetPatternForce(short DeviceNumber)
# SetPatternForce(short value, short DeviceNumber)
# GetPatternSelect(short DeviceNumber)
# SetPatternSelect(short value, short DeviceNumber)
# GetLoad4(short DeviceNumber)
# SetLoad4(short value, short DeviceNumber)


# class D4100:

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


# A Reset operation using DLL functions consists of
# 1. setting the Row Mode to NoOp [§ 6.2.10]
# 2. the Block Address to the desired block(s) [§ 6.2.6]
# 3. the Block Mode [§ 6.2.4]
# you may also need to set RST2BLKZ if using dual block [§ 6.2.8]
# and then calling Load Control [§ 6.2.1] to write these values to the DMD.
# I have found in practice that calling Load Control three times consecutively ensures that it writes over the USB interface. 