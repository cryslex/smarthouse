from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QThread
import pyttsx3
import voice
voice = voice.voice

sensors = []
for i in range(15):
    sensors.append('')

class SerialReadThread(QThread):
    def __init__(self, mainwindow, serial, parent=None):
        super().__init__()
        self.mainwindow = mainwindow
        self.serial = serial
        self.serial.readyRead.connect(self.onRead)

    def say(self, text):
        voice.say(text)
        voice.runAndWait()

    def onRead(self):
        rx = self.serial.readLine()
        rxs = str(rx, 'utf-8').strip()
        data = rxs.split(',')
        print(data)
        isError = False
        if len(data) >= 2:
            for item in data:
                if item == '':
                    isError = True
                    break
            if not isError:
                key = int(data[0])
                info = int(data[1])
                if sensors[key] != info:
                    if key == 0 and info == 1:
                        self.say('Внимание! Обнаружено движение на датчике движения номер 0.')
                        sensors[key] = info