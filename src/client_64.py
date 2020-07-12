from msl.loadlib import Client64

class D4100_USB_DLL(Client64):
    def __init__(self):
        super().__init__(module32='D4100_usb_32.py', quiet=True)

    def __getattr__(self, method32):
        def send(*args, **kwargs):
            return self.request32(method32, *args, **kwargs)
        return send


if __name__ == "__main__":
    from time import sleep
    sleeptime = 0.5

    d4100_dll = D4100_USB_DLL()
  
    devnum = d4100_dll.get_num_dev() - 1
    if devnum < 0:
        raise ValueError('No DMD devices found!')

    try:
        d4100_dll.global_reset(devnum)
        # for i in range(1,11):        
        #     print('on')
        #     d4100_dll.all_mirrors_on(devnum)
        #     sleep(sleeptime)
        #     print('off')
        # d4100_dll.all_mirrors_off(devnum)
        #     sleep(sleeptime)
        #     print(i)
    except KeyboardInterrupt:
        pass
