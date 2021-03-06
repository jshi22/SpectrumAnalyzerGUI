import time
import random
import bibliopixel
from bibliopixel.drivers.serial_driver import *
from bibliopixel.drivers.visualizer import *
from bibliopixel.led import *
import pyaudio
import wave
import numpy as np
from struct import unpack
from math import *
import bibliopixel.image as image

bibliopixel.log.setLogLevel(bibliopixel.log.DEBUG)
driver = DriverVisualizer(width=40, height=20, pixelSize=10)
led1 = LEDMatrix(driver, vert_flip=True)
texture1 = image.loadImage(led1, "texture2.jpg")
led1.setTexture(tex=texture1)
chunk = 4096

s = pyaudio.PyAudio()
sound = s.open(format = pyaudio.paInt16, channels = 2, rate = 44100, input = True, frames_per_buffer = chunk, input_device_index=2)
data = sound.read(chunk)

temp = [40]
for x in range(0,40):
    temp.append(0)

while True:
    data = sound.read(chunk)
    data = unpack("%dh"%(len(data)/2),data)
    data = np.array(data,dtype='h')
    data = abs(np.fft.rfft(data))
    data = data/7000
    y = 700
    for z in range(0,40):
        try:
            t = int(log(data[int(pow(1.00185,y))], 1.35)+(math.pow(y+100,2)/900000))
        except ValueError:
            t = 1

        if t > temp[z]:
            temp[z] = t
            
        led1.fillRect(z,0,1,int(temp[z]))
        y=y+83

        if temp[z] >= 1:
            factor = 2
            temp[z] = temp[z] - factor

    led1.update()
    led1.all_off()

sound.stop_stream()

sound.close()
s.terminate()
