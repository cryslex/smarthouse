from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice, QThread
from SpeechRecognizing import SpeechRecognitionThread
from SerialRead import SerialReadThread
import pyttsx3
from voice import voice
import sys

# Подключение к сериал порту

serial = QSerialPort()
serial.setBaudRate(115200)
portList = []
ports = QSerialPortInfo().availablePorts()

# Пополнение списка портов

for port in ports:
	portList.append(port.portName())

# Коды устройств

FAN = 2
LIGHT1 = 1

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = uic.loadUi("design.ui", self) # Загрузка интерфейса
        self.offUI()
        self.ui.setWindowTitle("Bot Ilon ( not Mask )") # Титл
        self.ui.setWindowIcon(QIcon('icon.ico')) # Иконка
        self.ui.ports.addItems(portList) # Загрузка листа портов
        # Клики кнопок
        self.ui.connectB.clicked.connect(self.connectPort)
        self.ui.disconnectB.clicked.connect(self.disconnectPort)
        self.ui.light1.stateChanged.connect(self.lightControl)
        self.ui.fan.stateChanged.connect(self.fanControl)
        self.SpeechRecognitionThread_instance = SpeechRecognitionThread(mainwindow = self)
        self.SpeechRecognitionThread_instance.start() # Старт отдельного потока для считывания голоса
        self.SerialReadThread_instance = SerialReadThread(mainwindow=self, serial=serial)
        # self.SerialReadThread_instance.start() - if you start SerialRead in another thread

    def offUI(self): # Выключение UI
        self.ui.light1.setDisabled(True)
        self.ui.fan.setDisabled(True)
        self.ui.disconnectB.setDisabled(True)

    def connectPort(self): # Подключение в порту
        serial.setPortName(self.ui.ports.currentText())
        isConnected = serial.open(QIODevice.ReadWrite)
        self.ui.light1.setEnabled(isConnected)
        self.ui.fan.setEnabled(isConnected)
        self.ui.disconnectB.setEnabled(isConnected)
        self.ui.connectB.setEnabled(not isConnected)

    def disconnectPort(self): # Отключение от порта
        serial.close()
        self.offUI()
        self.ui.connectB.setEnabled(True)

    def serialSend(self, data): # Отправка данных в порт
    	txs = ""
    	for val in data:
    		txs += str(val)
    		txs += ","
    	txs = txs[:-1]
    	txs += ";"
    	serial.write(txs.encode())

    def lightControl(self, val): # контроль света
    	if val == 2: val = 1
    	vals = [LIGHT1, val]
    	self.serialSend(vals)

    def fanControl(self, val): # контроль вентилятора
    	if val == 2: val = 1
    	vals = [FAN, val]
    	self.serialSend(vals)
    # запуск приложения
app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec())