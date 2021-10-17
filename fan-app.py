import serial
import time
import psutil
import sounddevice as sd
import numpy as np
from multiprocessing.dummy import Pool
import sys
from PyQt5.QtWidgets import *
import config





class ConfigOpener(QWidget):
    def __init__(self,name):
        super().__init__()
        self.button = QPushButton(name)
        self.layout = QGridLayout()
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        self.button.clicked.connect(self.opener)
    def opener(self):
        config.openConfig()

def sleepy(x):
    time.sleep(x)

def sendsound(x,indata, outdata, frames, time, status):
    print(time)

def choose(x):
    if(x[0]):
        sendspeed()
    else:
        sendsound(*x)

def Connect():
    while True:
        try:
            global arduino
            arduino = serial.Serial("COM3", 115200,timeout=.1)
            print("arduino plugged in!")
            return True

        except:
            print("failed to connect to arduino")
            time.sleep(1)

def PrintAr(bytez):
    try:
        arduino.write(bytez)
        return True
    except:
        Test()
        try:
            arduino.write(bytez)
            return True
        except:
            return False
def Test():
    while True:
        try:
            arduino.write(b'?')
            return False
        except:
            Connect()
            return True

def Check(st):
    try:
        read=arduino.read()
    except:
        Test()
        try:
            read=arduino.read()
        except:
            return False
    if(str(read).find(st)!=-1):
        return True
    return False

def WriteAr(strr):
    strr=bytes(strr,'utf-8')
    PrintAr(strr)
def ReadAr():
    try:
        read=arduino.readline()
        if(read):
            print(read)
        return True
    except:
        Test()
        try:
            read=arduino.readline()
            if(read):
                print(read)
            return True
        except:
            return False


def metermaker(volume):
    return ([('12f','1f2')[x>(volume)] for x in range(12)],[('f12','12f')[x>volume-12] for x in range(12)])[(volume)>12]








def monitor():
  ledlist=['[5]']+metermaker(lister[0])
  WriteAr("".join(ledlist))
  sleepy(.02)
  ledlist=['[6]']+metermaker(lister[1])
  WriteAr("".join(ledlist))
  sleepy(.02)
  ledlist=['[7]']+metermaker(lister[2])
  WriteAr("".join(ledlist))
  sleepy(.02)
  

def off():
  ledlist=['[5]']+['000']*12
  WriteAr("".join(ledlist))
  sleepy(.02)
  ledlist=['[6]']+['000']*12
  WriteAr("".join(ledlist))
  sleepy(.02)
  ledlist=['[7]']+['000']*12
  WriteAr("".join(ledlist))
  sleepy(.02)
allmodes={"monitor":monitor,"off":off}
currentmode=["monitor"]
offmode=["monitor"]
def turnoff():
  m=currentmode[0]
  if(m != "off"):
    currentmode.insert(0,"off")
def turnon():
  m=currentmode
  if(len(m)>1):
    currentmode.pop(0)
    
class onoffB(QWidget):
    def __init__(self,ontext,offtext,onfunc,offfunc,triggerfunc,oncolor="green",offcolor="red"):
        super().__init__()
        self.ontext=ontext
        self.offtext=offtext
        self.oncolor=oncolor
        self.offcolor=offcolor
        self.onfunc=onfunc
        self.offfunc=offfunc
        self.triggerfunc=triggerfunc
        self.button = QPushButton(ontext)
        self.button.setStyleSheet("background-color: "+oncolor)
        self.button.clicked.connect(self.click)
        self.layout = QGridLayout()
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
    def click(self):
        if(self.triggerfunc()):
            self.button.setText(self.offtext)
            self.button.setStyleSheet("background-color: "+self.offcolor)
            self.onfunc()
        else:
            self.button.setText(self.ontext)
            self.button.setStyleSheet("background-color: "+self.oncolor)
            self.offfunc()
def triggeronoff():
    return currentmode[0]=="off"

def appThread(x):
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle('QGridLayout')
    layout = QGridLayout()
    layout.addWidget(QPushButton('start'), 0, 0)
    onoff=onoffB("turn on","turn off",turnon,turnoff,triggeronoff)
    layout.addWidget(onoff, 0, 2)
    layout.addWidget(ConfigOpener('open config'), 1, 2)
    window.setLayout(layout)
    window.show()
    sys.exit(app.exec_())

def mainLoop(x):
    Test()
    while(not Check("!")):
        arduino.write(b'?')
        print("waiting for arduino to respond..")
        time.sleep(1)
    print("arduino awake!")
    ledlist=['r']
    while True:
      allmodes[currentmode[0]]()
      Test()


lister=[0,0,0]
def cpu(x):
  while True:
    lister[0]=psutil.cpu_percent(interval=.3)/(100/24)
def memory(x):
  while True:
    sleepy(.5)
    lister[1]=int(psutil.virtual_memory()[2])/(100/24)


def streamer(indata,outdata,frames,time,status):
  volume=int(np.linalg.norm(indata)*10)**.691
  lister[2]=volume

def audio(x):
  stream = sd.InputStream(callback=streamer)
  while True:
    with sd.Stream(callback=streamer):
      sd.sleep(10000)
    
    
    
def call(f):
    return f(0)
p = Pool(5)


p.map(call, [cpu,memory,mainLoop,audio,appThread])
