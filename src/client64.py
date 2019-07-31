from msl.loadlib import Client64

class D4100_DLL(Client64):
    def __init__(self):
        super().__init__(module32='D4100_usb_32.py', quiet=False)

    def __getattr__(self, method32):
        def send(*args, **kwargs):
            return self.request32(method32, *args, **kwargs)
        return send

class D4100:
    def __init__(self):
        self.dmd_type = None
        self.rows = 0
        self.cols = 0
    