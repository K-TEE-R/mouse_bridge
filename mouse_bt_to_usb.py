#!/usr/bin/python
#coding: utf-8

import evdev
import time

while True:
    hidg_dev = open('/dev/hidg0', mode='wb')
    if hidg_dev != None:
        print('Found HID gadget device')
        break
    print('Waiting for HID gadget device')
    time.sleep(1)

with open('/home/pi/work/test', mode='w') as f:
    f.write('boot')

while True:
    try:
        devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        if len(devices) == 0:
            print('No input devices are found. Waiting for next detection')
            time.sleep(1)
            
        for device in devices:
            key = 0
            print(device.fn, device.name, device.phys)
            if 'mouse' in device.name.lower():
                print('Mouse device {} is found.'.format(device.name))
            else:
                continue
            device = evdev.InputDevice(device.fn)
            for event in device.read_loop():
                print('type={}, code={}, value={}'.format(event.type, event.code, event.value))
                if event.type == evdev.ecodes.EV_REL:
                    if event.code == evdev.ecodes.REL_X:
                        if event.value >= 0:
                            barray = bytearray([key, event.value, 0, 0])
                            hidg_dev.write(barray)
                            hidg_dev.flush()
                        else:
                            barray = bytearray([key, 0xff + event.value, 0, 0])
                            hidg_dev.write(barray)
                            hidg_dev.flush()
                    if event.code == evdev.ecodes.REL_Y:
                        if event.value >= 0:
                            barray = bytearray([key, 0, event.value, 0])
                            hidg_dev.write(barray)
                            hidg_dev.flush()
                        else:
                            barray = bytearray([key, 0, 0xff + event.value, 0])
                            hidg_dev.write(barray)
                            hidg_dev.flush()
                    if event.code == evdev.ecodes.REL_WHEEL:
                        if event.value >= 0:
                            barray = bytearray([key, 0, 0, event.value])
                            hidg_dev.write(barray)
                            hidg_dev.flush()
                        else:
                            barray = bytearray([key, 0, 0, 0xff + event.value])
                            hidg_dev.write(barray)
                            hidg_dev.flush()
                elif event.type == evdev.ecodes.EV_KEY:
                     if event.value != 2:
                         print("send key code {}".format(event.value))
                         if event.value == 0:
                             key = 0
                         else:
                             key = event.code - 271
                         barray = bytearray([key, 0, 0, 0])
                         hidg_dev.write(barray)
                         hidg_dev.flush()
    except IOError as ioe:
        print(type(ioe))
    finally:
        print('No input devices are found. Waiting for next detection')
    

hidg_dev.close()
