import time
import random
import bibliopixel
from bibliopixel.drivers.visualizer import *
from bibliopixel.led import *
import pyaudio
import wave
import numpy as np
from struct import unpack
from math import *
import subprocess

class main(object):
    visw = 40
    vish = 20
    idevice = 2
    chunk = 1024
    yshift = 1
    bandc = 1.006
    logc = 1.35
    powshift = 100
    wscale = 90000
    freqrange = 25

    def initialize(self):
        cmdin = raw_input("Enter command: ")
        cmd = cmdin.split(" ")
        if cmd[0] == "start":
            subprocess.Popen(["cmd", "/k", "python", "volume.py"])
            self.startemu()
        elif cmd[0] == "height":
            self.vish = int(cmd[1])
            self.initialize()
        else:
            self.initialize()

    def startemu(self):
        i = initled()
        o = output()
        i.ledemu(self.visw, self.vish)
        o.mainloop(self.idevice, self.yshift, self.visw, self.bandc, self.logc, self.powshift, self.wscale, self.freqrange, self.chunk, i.led)

class initled(object):
    def ledemu(self, visw, vish):
        bibliopixel.log.setLogLevel(bibliopixel.log.DEBUG)
        driver = DriverVisualizer(width=visw, height=vish, pixelSize=10)
        self.led = LEDMatrix(driver, vert_flip=True)

    def ledsingle(self, visw, vish):
        coords1 = mapGen(10,5)
        bibliopixel.log.setLogLevel(bibliopixel.log.DEBUG)
        driver1 = DriverSerial(num = 50, type = LEDTYPE.WS2811, deviceID = 1)
        self.led = LEDMatrix(driver1, width=10, height=5, coordMap = coords1, rotation=MatrixRotation.ROTATE_180, masterBrightness=250, pixelSize=(1,1))

class output(object):
    def mainloop(self, idevice, yshift, visw, bandc, logc, powshift, wscale, freqrange, chunk, led):
        s = pyaudio.PyAudio()
        sound = s.open(format = pyaudio.paInt16, channels = 2, rate = 44100, input = True, frames_per_buffer = chunk, input_device_index=idevice)
        data = sound.read(chunk)
        while True:
            f = open("volume.txt", "r")
            vol = int(f.readline())
            f.close()
            data = sound.read(chunk)
            data = unpack("%dh"%(len(data)/2),data)
            data = np.array(data,dtype='h')
            data = abs(np.fft.rfft(data))
            data = data/vol
            y = yshift
            for z in range(0,visw):
                try:
                    t = int(log(data[int(pow(bandc,y))], logc)+(math.pow(y+powshift,2)/wscale))
                except ValueError:
                    t = 1

                led.fillRect(z,0,1,t,color=(255,255,255))
                y=y+freqrange

            led.update()
            led.all_off()

m = main()
m.initialize()