"""
example_load_frame_DMD.py 

Shows the basic methodology for loading an arbitrary bitmap image to a DMD
via the D4100_usb.dll. 

Alot of the logic for loading images and such can be wrapped into single function calls,
for now it is left explicit to make it more clear what operations occur within the DMD.

There are still some kinks to work out (loading idiosyncracies), and a unified interface 
for both 64 bit and native 32 bit runtimes, (see dev branch: <>). 
Seeing as I now have a usecase for this code again for a different project, 
I will be rectifying those in the coming couple of weeks or so. 
"""

import sys  # cli args to specify an image
from PIL import Image # image processing stuff 
import numpy as np # image processing/manip stuff
from client_64 import D4100DLL

def bmp_2_arr(path):
    """convert a bitmap to a np.ndarray of 8-bit values"""
    im = Image.open(path)
    # im.show()
    arr = np.asarray(im, dtype=np.uint8)
    return arr

def arr_2_bitstream(arr,bit_to_get=0):
    """
    convert an array from an aray representing an image into a bitstream to load into the DMD

    We grab each MSB from the image by default, 
    select what bit to pull from each 8-bit pixel value via the bit_to_get parameter. 
    Setting this parameter to 0 will grab all of the MSB values,
    Setting this parameter to 7 will grab all of the LSB values,
    Setting this parameter to n value inbeterrn will grab the nth bit values (where 0<=n<=7)
    """
    return np.packbits(np.unpackbits(arr, bitorder='big')[bit_to_get::8])

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# instantiate dll instance 
# behind the scenes is setting up a 32-bit process and the approrpiate IPC bridge
d4100_dll = D4100DLL()

# query DLL to see how many DMDs are connected to PC's USB hubs
# subtract 1 from result as a reuslt of the zero-indexing scheme 
devnum = d4100_dll.get_num_dev() - 1

# no DMDs found 
if devnum < 0:
    raise ValueError('No DMD devices found!')

# load image, prepare it to be loaded to DMD as a 1-bit binary image. 
# the image is provided via CLI arguement specifying a path that can be resolved from the current working directory
# either make the path absolute or properly specify the relative path
path = sys.argv[1]
# load image
arr = bmp_2_arr(path)
# prepare image as binary bitstream 
data = arr_2_bitstream(arr)

# frame loading takes at minumum 2 api calls, so go ahead and just split data 
# could just as well be done via indexing, but this makes things more straightforward to see in my head
data1, data2 = np.array_split(data,2)

# uncomment the next lines to ensure splitting is working
# d1 = Image.fromarray(data1.reshape(768//2,1024//8))
# d2 = Image.fromarray(data2.reshape(768//2,1024//8))
# d1.show()
# d2.show()

## configure DMD to display image
# disable test patterns
dmd.set_tpe_enable(devnum,0)
# optional - switch all mirrors to a known position
dmd.all_mirrors_off(devnum)
dmd.all_mirrors_on(devnum)

# set current row to top of device
current_row = 0
# optional - clear FIFOs
dmd.clear_fifos(devnum)

# For a description of what each mode entails, see table 12,14 of the DLPC410 controller datasheet
# https://ti.com/lit/ds/dlps024g/dlps024g.pdf
dmd.set_block_mode(devnum,0)
dmd.set_ns_flip(devnum,0)
dmd.set_row_mode(devnum,0b11)

# load image
# I find that loading each subblock via a row load, and then a block load is more reliable. 
# this is likely a latency tuning issue, and will probably be fixed by extending the minimal time between API calls. 
# Should have this fixed by the time this is needed again in the next couple of weeks.
dmd.load_data(devnum,data1[:128])
dmd.set_row_mode(devnum,0b01)
dmd.load_data(devnum,data1[128:])
# dmd.global_reset(devnum)

# load second half of frame
dmd.set_row_mode(devnum,0b10)
# subtract one for zero-indexing
dmd.set_row_address(devnum, 768//2 - 1) 
dmd.load_data(devnum,data2[:128])
dmd.set_row_mode(devnum,0b01)
dmd.load_data(devnum,data2[128:])

# initate Mirror Clocking Pulse (MCP)
# if not done, every ~ 10s a watchdog timer will force a MCP anyway
dmd.global_reset(devnum)

# park mirrors/float
dmd.float_mirrors(devnum)

# cleanup of resources is handled automatically on exit
# from here, on hardware of the DMD driver board simply ensure to hit the float/reset button before power down for best practice. 
