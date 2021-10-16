from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice, QThread
from SpeechRecognizing import SpeechRecognitionThread
from SerialRead import SerialReadThread
import pyttsx3
from voice import voice
import sys

serial = QSerialPort()
serial.setBaudRate(115200)
portList = []
ports = QSerialPortInfo().availablePorts()


for port in ports:
	portList.append(port.portName())

FAN = 2
LIGHT1 = 1

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = uic.loadUi("C:/Users/User/Desktop/Ilon/design.ui", self)
        self.offUI()
        self.ui.setWindowTitle("Bot Ilon ( not Mask )")
        self.ui.setWindowIcon(QIcon('icon.ico'))
        self.ui.ports.addItems(portList)
        self.ui.connectB.clicked.connect(self.connectPort)
        self.ui.disconnectB.clicked.connect(self.disconnectPort)
        self.ui.light1.stateChanged.connect(self.lightControl)
        self.ui.fan.stateChanged.connect(self.fanControl)
        self.SpeechRecognitionThread_instance = SpeechRecognitionThread(mainwindow = self)
        self.SpeechRecognitionThread_instance.start()
        self.SerialReadThread_instance = SerialReadThread(mainwindow=self, serial=serial)
        # self.SerialReadThread_instance.start() - if you start SerialRead in another thread
    def offUI(self):
        self.ui.light1.setDisabled(True)
        self.ui.fan.setDisabled(True)
        self.ui.disconnectB.setDisabled(True)
    def connectPort(self):
        serial.setPortName(self.ui.ports.currentText())
        isConnected = serial.open(QIODevice.ReadWrite)
        self.ui.light1.setEnabled(isConnected)
        self.ui.fan.setEnabled(isConnected)
        self.ui.disconnectB.setEnabled(isConnected)
        self.ui.connectB.setEnabled(not isConnected)

    def disconnectPort(self):
        serial.close()
        self.offUI()
        self.ui.connectB.setEnabled(True)

    def serialSend(self, data):
    	txs = ""
    	for val in data:
    		txs += str(val)
    		txs += ","
    	txs = txs[:-1]
    	txs += ";"
    	serial.write(txs.encode())

    def lightControl(self, val):
    	if val == 2: val = 1
    	vals = [LIGHT1, val]
    	self.serialSend(vals)

    def fanControl(self, val):
    	if val == 2: val = 1
    	vals = [FAN, val]
    	self.serialSend(vals)
app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec())