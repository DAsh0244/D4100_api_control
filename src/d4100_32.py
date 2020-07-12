import ctypes
from time import sleep
import os.path as osp
import os

class D4100_USB_DLL_MIXIN:
    """
    A partially implemented wrapper around the 32-bit D4100_usb.dll, thta implements the stock D4100 conteoller firmware api.
    For Specifics on API,see https://www.ti.com/lit/ug/dlpu039/dlpu039.pdf

    This is designed to be subclassed to define the property 'lib', allowing for cross use in dedeicated 32-bit processes and IPC processes. 
    As such, this cannot be used as is.
    """
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        # presupposes lib gets defined in super call. 
        self.lib.GetFPGARev.restype = ctypes.c_uint # force a return as a unint instead of typical int.
        # hard coded for now: 
        self.rows = 768
        self.cols = 1024
        # wait needed to let USB bus catchup
        self.wait = 0.005

    @staticmethod
    def _split_bytes(word):
        """
        Grab the lowest two bytes of a word
        
        Args:
            word (integer): >=16-bit word

        Returns:
            tuple: Upper and lower bytes in the order (upper,lower)
        """
        return (word&0xFF00)>>8,word&0x00FF

    @staticmethod
    def _split_wbytes(word):
        """
        split a 64-bit word into upper and lower 32-bit words
        Returns: 
        """
        return (word&0xFFFF0000)>>16,word&0x0000FFFF

    # short GetNumDev( )
    def get_num_dev(self):
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
        # sleep(1)
        self.load_control(devnum)
        self.load_control(devnum)
        self.load_control(devnum)
        self.set_block_mode(devnum,0b00)

    def _generate_array(self, inital_val=0):
        return  [[inital_val for x in range(self.cols)] for x in range(self.rows)] 

    def get_rows(self):
        return self.rows

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
            (self.load_data(devnum,row))
            # self.set_row_address(devnum, current_row)
            # sleep(self.wait)
            # print(self.get_row_address(devnum))
            # sleep(1)
        self.global_reset(devnum)  

    def all_mirrors_off(self,devnum):
        self.set_all_mirrors(devnum,0xff)

    def all_mirrors_on(self,devnum):
        self.set_all_mirrors(devnum,0x00)

    def bars(self,devnum, bars=2):
        block_size = self.rows//bars
        data = []
        for bar in range(bars):
            row =  [255*(bar%2) for x in range(block_size*self.cols//8)]
            print(len(row))
            data.extend(row)
        blocks = 2
        block_size = self.rows//blocks
        print(block_size)
        current_row = 0
        self.clear_fifos(devnum)
        self.global_reset(devnum)
        self.set_block_mode(devnum,0)
        self.set_ns_flip(devnum,0)
        self.set_row_mode(devnum,0b10)
        self.set_row_address(devnum,current_row)
        self.set_row_mode(devnum,0b01)
        # print(data)
        print(len(data))
        for i in range(blocks):
            (block_size*i*self.cols//8,self.cols*block_size*(i+1)//8)
            (self.load_data(devnum,data[block_size*i*self.cols//8:self.cols*block_size*(i+1)//8]))
            # print(data[block_size*i*self.cols//8:self.cols*block_size*(i+1)//8])
            # sleep(1)
        self.global_reset(devnum)

    # int LoadData(UCHAR* RowData, unsigned int length, short DMDType, short DeviceNumber)
    def load_data(self,devnum,data):
        """Load data onto DMD SRAM
        Configure addresses before calling this function

        Args:
            devnum (int): device number, see GetDevNum Documentation for what this should be. 
            data ([type]): array data to load onto DMD - each bit corresponds to an individual mirror, and is loaded in right to lef row order

        Returns:
            (int): return code of the LoadData API call. 
        """
        # get dev type
        dmd_type = self.get_dmd_type(devnum)
        # build data into ctypes uint8 array, take pointer to data for use in funciton call 
        dlen = len(data)
        b_data = (ctypes.c_ubyte * dlen)() # allocate array
        for i,val in enumerate(data): # initalize array to contents of data
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

# TODO: implement the following for full api support
# CONSIDER: passing a pointer is not viable between 64-32 bits...
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

class D4100_USB_DLL(D4100_USB_DLL_MIXIN):
    """
    A wrapper around the 32-bit D4100_usb.dll, thta implements the stock D4100 conteoller firmware api.
    For Specifics on API,see https://www.ti.com/lit/ug/dlpu039/dlpu039.pdf
    """
    def __init__(self):
        # The Server32 class has a 'lib' property that is a reference to the ctypes.CDLL object.
        self.lib = ctypes.CDLL(osp.join(osp.dirname(osp.abspath(__file__)), os.pardir, 'lib','D4100_usb.dll'))

if __name__ == "__main__":
    from PIL import Image
    import numpy as np
    import sys

    def bmp_2_arr(path):
        im = Image.open(path)
        # im.show()
        arr = np.asarray(im)
        return arr

    def arr_2_bitstream(arr):
        return np.packbits(np.unpackbits(arr)[::8])

    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    dmd = D4100_USB_DLL()
    devnum = dmd.get_num_dev() - 1
    if devnum < 0:
        raise ValueError('No DMD devices found!')

    path = sys.argv[1]
    # print(path)
    arr = bmp_2_arr(path)
    data = arr_2_bitstream(arr)
    
    data1, data2 = np.array_split(data,2)
    # d1 = Image.fromarray(data1.reshape(768//2,1024//8))
    # d2 = Image.fromarray(data2.reshape(768//2,1024//8))
    # d1.show()
    # d2.show()
    # input()
    dmd.set_tpe_enable(devnum,0)
    dmd.all_mirrors_off(devnum)
    dmd.all_mirrors_on(devnum)
    current_row = 0
    # sleep(5)
    # dmd.clear_fifos(devnum)
    dmd.set_block_mode(devnum,0)
    dmd.set_ns_flip(devnum,1)
    dmd.set_row_mode(devnum,0b11)

    # sleep(1)
    dmd.load_data(devnum,data1[:128])
    dmd.set_row_mode(devnum,0b01)
    dmd.load_data(devnum,data1[128:])
    # print(dmd.get_row_address(devnum))
    dmd.global_reset(devnum)
    dmd.set_row_mode(devnum,0b10)
    dmd.set_row_address(devnum, 768//2 - 1)
    dmd.load_data(devnum,data2[:128])
    dmd.set_row_mode(devnum,0b01)
    dmd.load_data(devnum,data2[128:])
    dmd.global_reset(devnum)

    # for row in range(768):
    #     print(row)
    #     dmd.set_block_mode(devnum,0)
    #     # dmd.global_reset(devnum)
    #     dmd.set_row_mode(devnum,0b10)
    #     dmd.set_row_address(devnum,row)
    #     # sleep(1)
    #     dmd.set_row_mode(devnum,0b01)
    #     dmd.load_data(devnum,data[128*row:(128*row)+128])
    #     # sleep(0.1)
    #     dmd.global_reset(devnum)
    dmd.global_reset(devnum)
    # print(list(data1[:]))
    # input()
    # print(dmd.get_row_address(devnum))
    # print(dmd.get_block_address(devnum))
    # (dmd.load_data(devnum,data1))

    # current_row=768//2
    # dmd.set_block_mode(devnum,0)
    # dmd.set_ns_flip(devnum,0)
    # dmd.set_row_mode(devnum,0b10)
    # dmd.set_row_address(devnum,current_row)
    # dmd.set_row_mode(devnum,0b01)
    # print(dmd.get_row_address(devnum))
    # print(dmd.get_block_address(devnum))
    # print(list(data2[:]))
    # input()
    # (dmd.load_data(devnum,data2))
    # sleep(1)
    # dmd.global_reset(devnum)
    # print(dmd.get_row_address(devnum))
    # print(dmd.get_block_address(devnum))
    dmd.global_reset(devnum)
    sleep(1)
    dmd.global_reset(devnum)
    # dmd.global_reset(devnum)
    # dmd.global_reset(devnum)
