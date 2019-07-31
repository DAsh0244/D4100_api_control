import ctypes
from msl.loadlib import Server32
from time import sleep

class D4100_USB_DLL(Server32):
    """A wrapper around a 32-bit C++ library, 'cpp_lib32.dll', that has an 'add' function."""

    def __init__(self, host, port, quiet=False, **kwargs):
        # Load the 'cpp_lib32' shared-library file using ctypes.CDLL.
        super().__init__('../lib/D4100_usb.dll', 'cdll', host, port, quiet)
        self.lib.GetFPGARev.restype = ctypes.c_uint
        self.rows = 768
        self.cols = 1024
        self.wait = 0.005

    @staticmethod
    def _split_bytes(rev):
        return (rev&0xFF00)>>8,rev&0x00FF

    @staticmethod
    def _split_wbytes(rev):
        return (rev&0xFFFF0000)>>16,rev&0x0000FFFF

    # short GetNumDev( )
    def get_num_dev(self):
        # The Server32 class has a 'lib' property that is a reference to the ctypes.CDLL object.
        # The shared library’s 'add' function takes two integers as inputs and returns the sum.
        print('counting num dev')
        return self.lib.GetNumDev()

    # short GetDMDTYPE(short DeviceNumber)
    def get_dmd_type(self, devnum):
        return self.lib.GetDMDTYPE(devnum)

    # unsigned int GetDLLRev( )
    def get_dll_rev(self):
        rev = self.lib.GetDLLRev()
        return self._split_wbytes(rev)

    # unsigned int GetDriverRev(short DeviceNumber)
    def get_driver_rev(self,devnum):
        rev = self.lib.GetDriverRev(devnum)
        return (rev&0xFF000000)>>24,(rev&0x00FF0000)>>16,(rev&0x0000FF00)>>8,(rev&0x000000FF)

    # unsigned int GetFirmwareRev(short DeviceNumber)
    def get_firmware_rev(self,devnum):
        rev = self.lib.GetFirmwareRev(devnum)
        return self._split_bytes(rev)

    # unsigned int GetFPGARev(short DeviceNumber)
    def get_fpga_rev(self,devnum):        
        rev = self.lib.GetFPGARev(devnum)
        return rev&0xFF, (rev&0xF00)>>8, (rev&0xF000)>>12

    # short int GetUsbSpeed(short DeviceNumber)
    def get_usb_speed(self, devnum):
        speed = self.lib.GetUsbSpeed(devnum)
        return speed

    # short GetDDCVERSION(short DeviceNumber)
    def get_ddc_version(self,devnum):
        ret = self.lib.GetDDCVERSION(devnum)
        return ret&0b0111

    # short GetGPIO(short DeviceNumber)
    def get_gpio(self,devnum):
        ret = self.lib.GetGPIO(devnum)
        return (ret&0b11100)>>2

    # short SetGPIO(short value, short DeviceNumber)
    def set_gpio(self,devnum,gpio_val):
        return self.lib.SetGPIO(gpio_val,devnum)

    # short GetTPGEnable(short DeviceNumber)
    def get_tpe_enable(self,devnum):
        ret = self.lib.GetTPGEnable(devnum)
        return ret

    # short SetTPGEnable(short value, short DeviceNumber)
    def set_tpe_enable(self,devnum,val):
        self.lib.SetTPGEnable(val,devnum)

    # short GetPatternForce(short DeviceNumber)
    def get_pattern_force(self,devnum):
        ret = self.lib.GetPatternForce(devnum)
        return ret
    # short SetPatternForce(short value, short DeviceNumber)
    def set_pattern_force(self,devnum,val):
        self.lib.SetTPGEnable(val,devnum)

    # short GetPatternSelect(short DeviceNumber)
    def get_pattern_select(self,devnum):
        ret = self.lib.GetPatternSelect(devnum)
        return ret

    # short SetPatternSelect(short value, short DeviceNumber)
    def set_pattern_select(self,devnum,val):
        return self.lib.SetPatternSelect(val,devnum)

    # short GetPWRFLOAT(short DeviceNumber)
    def get_pwr_float(self,devnum):
        ret = self.lib.GetPWRFLOAT(devnum)
        return ret

    # short SetPWRFLOAT(short value, short DeviceNumber)
    def set_pwr_float(self,devnum,val):
        return self.lib.SetPWRFLOAT(val,devnum)

    # short GetRowMd(short DeviceNumber)
    def get_row_mode(self,devnum):
        return self.lib.GetRowMd(devnum)

    # short SetRowMd(short value, short DeviceNumber)
    def set_row_mode(self,devnum,val):
        return self.lib.SetRowMd(val, devnum)

    # short GetBlkMd(short DeviceNumber)
    def get_block_mode(self,devnum):
        return self.lib.GetBlkMd(devnum)

    # short SetBlkMd(short value, short DeviceNumber)
    def set_block_mode(self,devnum,val):
        return self.lib.SetBlkMd(val,devnum)

    # short GetBlkAd(short DeviceNumber)
    def get_block_address(self,devnum):
        return self.lib.GetBlkAd(devnum)

    # short SetBlkAd(short value, short DeviceNumber)
    def set_block_address(self,devnum,val):
        return self.lib.SetBlkAd(val,devnum)

    # short GetRowAddr(short DeviceNumber)
    def get_row_address(self,devnum):
        return self.lib.GetRowAddr(devnum)

    # short SetRowAddr(short value, short DeviceNumber)
    def set_row_address(self,devnum,val):
        return self.lib.SetRowAddr(val,devnum)

    # short LoadControl(short DeviceNumber)
    def load_control(self,devnum):
        return self.lib.LoadControl(devnum)


    def float_mirrors(self,devnum):
        self.set_row_mode(devnum,0b00)
        self.set_block_mode(devnum,0b11)
        self.set_block_address(devnum,0b1100)
        self.load_control(devnum)
        self.load_control(devnum)
        self.load_control(devnum)

    def global_reset(self,devnum):
        """
        https://e2e.ti.com/support/dlp/f/94/t/819526
        A Reset operation using DLL functions consists of
        1. setting the Row Mode to NoOp [§ 6.2.10]
        2. the Block Address to the desired block(s) [§ 6.2.6]
        3. the Block Mode [§ 6.2.4]
        you may also need to set RST2BLKZ if using dual block [§ 6.2.8]
        and then calling Load Control [§ 6.2.1] to write these values to the DMD.
        I have found in practice that calling Load Control three times consecutively ensures that it writes over the USB interface. 

        
        Arguments:
            devnum {[type]} -- [description]
        """
        self.set_row_mode(devnum,0b00)
        self.set_block_mode(devnum,0b11)
        self.set_block_address(devnum,0b1000)
        self.load_control(devnum)
        self.set_block_mode(devnum,0b00)
        self.load_control(devnum)
        self.load_control(devnum)

    def _generate_array(self, inital_val=0):
        return  [[inital_val for x in range(self.cols)] for x in range(self.rows)] 

    def set_wait(self,wait):
        self.wait=wait

    def set_all_mirrors(self,devnum,val):
        self.set_tpe_enable(devnum,0)
        blocks = 2
        block_size = self.rows//blocks
        current_row = 0
        row = [val for x in range(block_size*self.cols)]
        # load rows
        self.clear_fifos(devnum)
        self.global_reset(devnum)
        self.set_block_mode(devnum,0)
        self.set_ns_flip(devnum,0)
        self.set_row_mode(devnum,0b10)
        self.set_row_address(devnum,current_row)
        self.set_row_mode(devnum,0b01)
        for i in range(blocks):
            # current_row += block_size
            print(self.load_data(devnum,row))
            # self.set_row_address(devnum, current_row)
            # sleep(self.wait)
            # print(self.get_row_address(devnum))
            # sleep(1)
        self.global_reset(devnum)    

    def all_mirrors_off(self,devnum):
        self.set_all_mirrors(devnum,0)

    def all_mirrors_on(self,devnum):
        self.set_all_mirrors(devnum,255)

    # def vertical_bars(self,devnum):
    #     data = 

    # int LoadData(UCHAR* RowData, unsigned int length, short DMDType, short DeviceNumber)
    def load_data(self,devnum,data):
        dmd_type = self.get_dmd_type(devnum)
        dlen = len(data)
        b_data = (ctypes.c_ubyte * dlen)()
        for i,val in enumerate(data):
            b_data[i] = val
        # print(b_data[:8],len(b_data))
        return self.lib.LoadData(ctypes.byref(b_data),dlen,dmd_type,devnum)
    
    # short ClearFifos(short DeviceNumber)
    def clear_fifos(self,devnum):
        return self.lib.ClearFifos(devnum)

    # short SetNSFLIP(short value, short DeviceNumber)
    def set_ns_flip(self,devnum,val):
        return self.lib.SetNSFLIP(val,devnum)

    # short GetNSFLIP(short DeviceNumber)
    def get_ns_flip(self,devnum):
        return self.lib.GetNSFLIP(devnum)

# int program_FPGA(UCHAR* write_buffer, long write_size, short int DeviceNumber)
# int GetDescriptor(int*, short DeviceNum)
# short SetRST2BLKZ(short value, short DeviceNumber)
# short GetRST2BLKZ(short DeviceNumber)
# short SetCOMPDATA(short value, short DeviceNumber)
# short GetCOMPDATA(short DeviceNumber)
# short SetWDT(short value, short DeviceNumber)
# short GetWDT(short DeviceNumber)
# short SetEXTRESETENBL(short value, short DeviceNumber)
# short GetEXTRESETENBL(short DeviceNumber)
# short GetRESETCOMPLETE(int waittime, short int DeviceNumber)
# short SetGPIORESETCOMPLETE(short DeviceNumber)
# short GetSWOverrideEnable(short DeviceNumber)
# short SetSWOverrideEnable(short value, short DeviceNumber)
# short GetSWOverrideValue(short DeviceNumber)
# short SetSWOverrideValue(short value, short DeviceNumber)
# short GetLoad4(short DeviceNumber)
# short SetLoad4(short value, short DeviceNumber)

