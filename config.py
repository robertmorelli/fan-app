import sys
import random
import json
from PyQt5.QtWidgets import *
updates={}
f=open("config.json",'r')
updates=json.load(f)
def updatePins(thing):
    for i,pin in enumerate(updates['pins']):
        thing.addWidget(pinButtons(*pin), i+3, 0)

      
class updateButton(QWidget):
    def __init__(self,name):
        super().__init__()
        self.button = QPushButton(name)
        self.layout = QGridLayout()
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.button.clicked.connect(self.save)


    def save(self):
        f=open("config.json",'r')
        fig=json.load(f)
        f.close()
        fig.update(updates)
        f=open("config.json",'w')
        f.writelines(json.dumps(fig))

class pinButtons(QWidget):
    def __init__(self,pin,name):
        super().__init__()
        self.btn1 = QPushButton("edit")
        self.layout = QGridLayout()
        self.layout.addWidget(self.btn1,0,0)
        self.btn2 = QPushButton("edit")
        self.layout.addWidget(self.btn2,0,2)
        self.le1 = QLineEdit()
        self.le2 = QLineEdit()
        self.le1.setText(str(pin))
        self.le2.setText(name)
        self.le1.setReadOnly(True)
        self.le2.setReadOnly(True)
        self.layout.addWidget(self.le1,0,1)
        self.layout.addWidget(self.le2,0,3)
        
        self.setLayout(self.layout)
        self.btn1.clicked.connect(self.opener)


    def opener(self):
        self.sc=NewDialog(self)
        self.sc.show()

class addpin(QWidget):
    def __init__(self,parent = None):
        super().__init__()
        self.btn1 = QPushButton("add pin")
        self.layout = QGridLayout()
        self.layout.addWidget(self.btn1,0,0)
        self.le1 = QLineEdit()
        self.le2 = QLineEdit()
        self.layout.addWidget(self.le1,0,1)
        self.layout.addWidget(self.le2,0,2)
        self.setLayout(self.layout)



        
class inputdialogdemo(QWidget):
   def __init__(self, parent = None):
      super(inputdialogdemo, self).__init__(parent)
      layout = QFormLayout()
      self.btn1 = QPushButton("edit COM")
      self.btn1.clicked.connect(self.gettext)
      self.le1 = QLineEdit()
      self.le1.setReadOnly(True)
      layout.addRow(self.btn1,self.le1)
      self.setLayout(layout)
      f=open("config.json",'r')
      fig=json.load(f)
      self.le1.setText(fig['port'])
   def gettext(self):
      text, ok = QInputDialog.getInt(self, 'COM', 'select COM port:')
		
      if ok:
         self.le1.setText("COM"+str(text))
         updates['port']="COM"+str(text)
	

class NewDialog(QWidget):
  def __init__(self,parent):
    super(NewDialog, self).__init__(parent)
    self.setLayout(QFormLayout())
    self.show()

def openConfig():
    con = QDialog()
    con.setWindowTitle('config')
    layout = QGridLayout()
    layout.addWidget(QLabel('port configuration:'),0,0)
    layout.addWidget(inputdialogdemo(), 1, 0)
    layout.addWidget(updateButton('Update File') ,0, 2)
    layout.addWidget(QLabel('pin configuration:'),2,0)
    layout.addWidget(addpin("hey"),7,0)
    updatePins(layout)
    
    con.setLayout(layout)
    con.show()
    con.exec_()

