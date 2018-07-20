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
numPoints = 11
Vhi = 10
Vneg = -Vhi
currProt = 0.125
step = Vhi/(numPoints - 1)
mux = [1]
each = ['V1']
timeBegin = datetime.datetime.now()
elapse = 4*len(mux)*len(each)*(timeStep*numPoints) + 3*len(mux)*len(each)*14.5
timeEnd = timeBegin + datetime.timedelta(0,elapse)
print("Measurement Begin: {:%A, %d %B %Y %H:%M:%S}".format(timeBegin))
print("Measurement End:   {:%A, %d %B %Y %H:%M:%S}".format(timeEnd))

for i in mux:
    for k in each:
        sampleName = '180719_Something'+str(i)+'-'+str(k)
        startTimeStr = OLEDTools.stringTime()
        print("Time: {}, Sample: {} ".format(startTimeStr,sampleName),end='')
        outName = sampleName+'_'+startTimeStr+'.csv'

        # Initializing mux switch, selecting device
        time.sleep(0.5)
        ser.write(b'+0')
        time.sleep(2)
        ser.write(str.encode('-' + str(i)))
        time.sleep(2)

        # Sweep zero, hi, zero, low, zero
        x = OLEDTools.IVBSweep(0, Vhi, step, timeStep, currProt,1)
        OLEDTools.writeIVB(outName,x)
        print('Saved: 1...',end='')
        y = OLEDTools.IVBSweep(Vhi, Vneg, step, timeStep, currProt,0)
        OLEDTools.writeIVB(outName,x+y)
        print('2...3...',end='')
        z = OLEDTools.IVBSweep(Vneg, 0, step, timeStep, currProt,0)
        totalIVB = x + y + z
        OLEDTools.writeIVB(outName,totalIVB)
        print('4...',end='')

# Turn off SMU output, close device connection
OLEDTools.SMUclose()
