from psu_control import Keithley2220G1
from client64 import D4100DLL


PSU_PORT = 'COM11'
PSU_ADDR = 8
RESET_CHANNEL = 1
BIAS_CHANNEL = 2
ON_FLOAT_LEVELS = (17,  17.6) # reset, bias
ON_OFF_LEVELS = (24, 27) # reset, bias

import winsound
f_on_float = 1000  # Set Frequency To 2500 Hertz
f_float = 2000
f_off = 3000
f_on_off = 4000
duration = 1000  # Set Duration To 1000 ms == 1 second


def beep(freq):
    pass
    # winsound.Beep(freq,duration)


if __name__ == "__main__":    
    psu = Keithley2220G1(port=PSU_PORT,addr=PSU_ADDR,enforce_addr=True)
    psu.set_current(BIAS_CHANNEL, 65e-3)
    psu.set_current(RESET_CHANNEL, 65e-3)
    d4100_dll = D4100DLL()
    
    devnum = d4100_dll.get_num_dev() - 1
    if devnum < 0:
        raise ValueError('No DMD devices found!')

    from time import sleep

    # wait_func = lambda:sleep(0.11)
    wait_func = lambda : None
    # wait_func = input

    while True:
        try:
            # set levels to on/float
            psu.set_voltage(RESET_CHANNEL, ON_FLOAT_LEVELS[0])
            psu.set_voltage(BIAS_CHANNEL, ON_FLOAT_LEVELS[1])
            # sleep(0.05)

            # reset pulse
            # d4100_dll.float_mirrors(devnum)
            # beep(f_float)
            # d4100_dll.global_reset(devnum)

            # # all ON
            # d4100_dll.all_mirrors_on(devnum)
            # print(f'All Mirrors ON State - Capture Image\n BIAS={ON_FLOAT_LEVELS[1]}, RESET=-{ON_FLOAT_LEVELS[0]}')
            # wait_func()

            # all FLOAT
            d4100_dll.all_mirrors_off(devnum)
            print(f'All Mirrors FLOAT State - Capture Image\n BIAS={ON_FLOAT_LEVELS[1]}, RESET=-{ON_FLOAT_LEVELS[0]}')
            wait_func()

            # all ON
            d4100_dll.all_mirrors_on(devnum)
            beep(f_on_float)
            print(f'All Mirrors ON State - Capture Image\n BIAS={ON_FLOAT_LEVELS[1]}, RESET=-{ON_FLOAT_LEVELS[0]}')
            wait_func()
            # wait_func()

            # sleep(0.5)

            # set levels to on/off
            psu.set_voltage(RESET_CHANNEL, ON_OFF_LEVELS[0])
            psu.set_voltage(BIAS_CHANNEL, ON_OFF_LEVELS[1])
            # sleep(0.05)
            
            # d4100_dll.global_reset(devnum)


            # # # all ON
            # d4100_dll.all_mirrors_on(devnum)
            # print(f'All Mirrors ON State - Capture Image\n BIAS={ON_OFF_LEVELS[1]}, RESET=-{ON_OFF_LEVELS[0]}')
            # wait_func()

            # all OFF
            d4100_dll.all_mirrors_off(devnum)
            beep(f_off)
            print(f'All Mirrors OFF State - Capture Image\n BIAS={ON_OFF_LEVELS[1]}, RESET=-{ON_OFF_LEVELS[0]}')
            wait_func()

            # all ON
            d4100_dll.all_mirrors_on(devnum)
            print(f'All Mirrors ON State - Capture Image\n BIAS={ON_OFF_LEVELS[1]}, RESET=-{ON_OFF_LEVELS[0]}')
            wait_func()
            # wait_func()


            # # set levels to on/float
            # psu.set_voltage(RESET_CHANNEL, ON_FLOAT_LEVELS[0])
            # psu.set_voltage(BIAS_CHANNEL, ON_FLOAT_LEVELS[1])
            # # sleep(0.5)

            # # # all FLOAT
            # d4100_dll.all_mirrors_off(devnum)
            # beep(f_float)
            # print(f'All Mirrors FLOAT State - Capture Image\n BIAS={ON_FLOAT_LEVELS[1]}, RESET=-{ON_FLOAT_LEVELS[0]}')
            # wait_func()

            # psu.set_voltage(RESET_CHANNEL, ON_OFF_LEVELS[0])
            # psu.set_voltage(BIAS_CHANNEL, ON_OFF_LEVELS[1])
            # sleep(0.1)

            # # all ON
            # d4100_dll.all_mirrors_on(devnum)
            # beep(f_on_off)
            # print(f'All Mirrors ON State - Capture Image\n BIAS={ON_OFF_LEVELS[1]}, RESET=-{ON_OFF_LEVELS[0]}')
            # wait_func()

        except KeyboardInterrupt:
            break
    # reset to on/float
    psu.set_voltage(RESET_CHANNEL, ON_FLOAT_LEVELS[0])
    psu.set_voltage(BIAS_CHANNEL, ON_FLOAT_LEVELS[1])

