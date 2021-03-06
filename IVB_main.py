import datetime
import serial.tools.list_ports
import numpy
import math
import serial
import sys
import os
import time
sys.path.append('C:\\Users\\Morty\\IdeaProjects\\OLED_Tools')
import OLEDTools

# Opening serial communication to Arduino multiplexer switch
ser = serial.Serial('COM3', 9600, timeout=0)
# Opening connection to Keysight B2901A SMU
#rm = visa.ResourceManager()
#B2901A_address = rm.list_resources()[0]
#SMU = rm.open_resource(B2901A_address)

# Creating / Navigating to the correct data directory (new one for each day)
os.chdir('C:\\Users\\Morty\\Documents\\OLED_IVB_Data')
print("Current Directory: {}".format(os.getcwd()))
OLEDTools.makeTodayDir()
# decayTime = 600

# Initializing sweep parameters
timeStep = .05
currProt = 50E-3
#decayTime = 5
mux = [1,3,4,5,6,7,8]
#Vto = [""]*8
Vto = [-3.86,-3.86,-3.86,-3.86,-3.86,-3.86,-3.86]
print(Vto)
# for i in mux:
#     time.sleep(0.5)
#     ser.write(b'+0')
#     time.sleep(2)
#     ser.write(str.encode('-' + str(i)))
#     time.sleep(2)
#     Vto[i-1] = OLEDTools.findTurnOnVoltage(-3,-4.5,.01,25e-3,3e-8)
#     print(Vto)
#     time.sleep(2)
#     ser.write(str.encode('+' + str(i)))
#     time.sleep(2)
# print(Vto)
each = ['V1']
timeBegin = datetime.datetime.now()
print("Measurement Begin: {:%A, %d %B %Y %H:%M:%S}".format(timeBegin))

for i in mux:
    for k in each:
        negVoltSweep = list(reversed(list((-1*numpy.logspace(-8,math.log10(10),num=400)))))
        #lowVoltSweep = list(numpy.logspace(-8,math.log10(-1*float(Vto[i-1])),num=800))
        #voltSweep = list(numpy.logspace(math.log10(-1*float(Vto[i-1])),math.log10(10),num=200))
        voltSweep = list(numpy.logspace(-8,math.log10(10),num=400))
        #voltSweepTotal = negVoltSweep + lowVoltSweep + voltSweep
        voltSweepTotal = negVoltSweep + voltSweep
        voltSweepTotal = [-x for x in voltSweepTotal]
        sampleName = '210302cAFM50%'+str(i)+'-'+str(k)
        startTimeStr = OLEDTools.stringTime()
        print("Time: {}, Sample: {} ".format(startTimeStr,sampleName))
        outName = sampleName+'_'+startTimeStr+'.csv'
        outDecayName = sampleName+'_Decay_'+startTimeStr+'.csv'

        # Initializing mux switch, selecting device
        time.sleep(0.5)
        ser.write(b'+0')
        time.sleep(2)
        ser.write(str.encode('-' + str(i)))
        time.sleep(2)

        # Reverse Biasing:
        #OLEDTools.biasVoltsTime(30,15)

        # print("Decay Test:")
        # ts = OLEDTools.currDecay(-.0001,decayTime)
        # if ts != "fail":
        #     OLEDTools.writeIVBDecay(outDecayName,ts)
        #OLEDTools.findTurnOnVoltage(15,20,.005,5e-3,3e-8)
        if 1:
            print("IV Test: ",end='')
            # Sweep zero, hi, zero, low, zero
            w = OLEDTools.IVBSweep(0,currProt,voltSweepTotal)
            print("foo")
            OLEDTools.writeIVB(outName,w)
            print("foo2")

        time.sleep(2)
        print("foo3")
        ser.write(str.encode('+' + str(i)))
        print("foo4")
        time.sleep(2)
# Turn off SMU output, close device connection
OLEDTools.SMUclose()
