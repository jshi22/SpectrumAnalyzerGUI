import time
import random
import bibliopixel
from bibliopixel.drivers.serial_driver import *
from bibliopixel.led import *
import pyaudio
import wave
import numpy as np
from struct import unpack
import math

bibliopixel.log.setLogLevel(bibliopixel.log.DEBUG)
driver1 = DriverSerial(num = 600, type = LEDTYPE.WS2811, deviceID = 1)
driver2 = DriverSerial(num = 650, type = LEDTYPE.WS2811, deviceID = 2)
led1 = LEDMatrix(driver1, width=50, height=12, coordMap = None, rotation=MatrixRotation.ROTATE_180, masterBrightness=50, pixelSize=(1,1))
led2 = LEDMatrix(driver2, width=50, height=13, coordMap = None, rotation=MatrixRotation.ROTATE_180, masterBrightness=50, pixelSize=(1,1))
chunk = 4096

s = pyaudio.PyAudio()

sound = s.open(format = pyaudio.paInt16, channels = 2, rate = 44100, input = True, frames_per_buffer = chunk, input_device_index=2)

data = sound.read(chunk)
while True:
    data = sound.read(chunk)
    data = unpack("%dh"%(len(data)/2),data)
    data = np.array(data,dtype='h')
    data = abs(np.fft.rfft(data))
    data = data/12000
    y = 0
    for z in range(0,50):
        try:
            t = int(math.log(data[y], 1.4))
        except ValueError:
            t = 0

        if t>23:
            led1.fillRect(z,0,1,t,color=(255,0,0))
            led2.fillRect(z,0,1,t-11,color=(255,0,0))
        elif t>22:
            led1.fillRect(z,0,1,t,color=(255,165,0))
            led2.fillRect(z,0,1,t-11,color=(255,165,0))
        elif t>21:
            led1.fillRect(z,0,1,t,color=(255,255,0))
            led2.fillRect(z,0,1,t-11,color=(255,255,0))    
        elif t>15:
            led1.fillRect(z,0,1,t,color=(0,255,0))
            led2.fillRect(z,0,1,t-11,color=(0,255,0))
        elif t>12:
            led1.fillRect(z,0,1,t,color=(0,0,255))
            led2.fillRect(z,0,1,t-11,color=(0,0,255))
        else:
            led1.fillRect(z,0,1,t,color=(0,0,255))
            led2.fillRect(z,0,1,t-11,color=(0,0,0))
        
        y = y + 4

    led1.update()
    led2.update()
    led1.all_off()
    led2.all_off()

sound.stop_stream()

sound.close()
s.terminate()
