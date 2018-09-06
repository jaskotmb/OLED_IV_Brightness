import datetime
import serial.tools.list_ports
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

# Initializing sweep parameters
timeStep = .05
Vhi = 5
Vneg = -11
currProt = 25E-3
decayTime = 600
stepup = 200
stepdown = 800
mux = [5,6,7,8]
each = ['V2']
timeBegin = datetime.datetime.now()
print("Measurement Begin: {:%A, %d %B %Y %H:%M:%S}".format(timeBegin))

for i in mux:
    for k in each:
        sampleName = '180828Dv18'+str(i)+'-'+str(k)
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

        # print("Decay Test:")
        # ts = OLEDTools.currDecay(-.1E-3,decayTime)
        # if ts != "fail":
        #     OLEDTools.writeIVBDecay(outDecayName,ts)
        if 1:
            print("IV Test: ",end='')
            # Sweep zero, hi, zero, low, zero
            w = OLEDTools.IVBSweep(0, Vhi, stepup, currProt,1)
            OLEDTools.writeIVB(outName,w)
            print('Saved: 1...',end='')
            x = OLEDTools.IVBSweep(Vhi, 0, stepup, currProt,1)
            OLEDTools.writeIVB(outName,w+x)
            print('2...',end='')
            y = OLEDTools.IVBSweep(0, Vneg, stepdown, currProt,1)
            OLEDTools.writeIVB(outName,w+x+y)
            print('3...',end='')
            z = OLEDTools.IVBSweep(Vneg, 0, stepdown, currProt,1)
            totalIVB = w + x + y + z
            OLEDTools.writeIVB(outName,totalIVB)
            print('4...')


        time.sleep(2)
        ser.write(str.encode('+' + str(i)))
        time.sleep(2)
# Turn off SMU output, close device connection
OLEDTools.SMUclose()
