from PyQt5.QtCore import QThread

import speech_recognition as sr
import pyttsx3
import webbrowser
import voice
voice = voice.voice

import os
import sys

from SerialRead import SerialReadThread

webbrowser.register('Chrome', None, webbrowser.BackgroundBrowser('C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'))

commands = {
    ("включить", "включи", "включил", "включив", "вруби", "включай"):
        {
            "вентилятор":    ["вентилятор", "вертушку", "обдув"],
            "свет":          ["свет", "освещение", "светодиод"],
			"всё":           ["всё"]
        },
    ("выключить", "выключи", "выключил", "выключив", "выруби", "выключай"):
		{
			"вентилятор":    ["вентилятор", "вертушку", "обдув"],
			"свет":          ["свет", "освещение", "светодиод"],
			"всё":           ["всё"]
		},
	("открыть", "открой", "open"):
		{
			"youtube":       ["youtube", "ютубчик", "видео"],
			"калькулятор":   ["калькулятор", "бульбулятор"],
			"блокнот":       ["блокнот", "записи", "блокнотик", "блокноты", "текст"],
			"google":        ["google", "поисковик", "браузер"],
			"яндекс":        ["яндекс"],
			"вк":            ["вконтакте", "vk"],
			"одноклассники": ["одноклассники"]
		}
}

exceptions = {
	"посчитай": ["считай", "реши"],
}

class SpeechRecognitionThread(QThread):
	def __init__(self, mainwindow, parent=None):
		super().__init__()
		self.mainwindow = mainwindow
		voice.say("Здравствуйте, слушаю Вас.")
		voice.runAndWait()
		self.mainwindow.ui.microphoneImage.setEnabled(False)
	def run(self):
		def listen():
			r = sr.Recognizer()
			with sr.Microphone() as source:
				print("Скажи что-нибудь")
				self.mainwindow.ui.microphoneImage.setEnabled(True)
				r.pause_thresold = 0.3
				r.adjust_for_ambient_noise(source, duration = 0.6)
				audio = r.listen(source)
				# self.mainwindow.ui.microphoneImage.setEnabled(True)
				try:
					task = r.recognize_google(audio, language = "ru-RU").lower()
					print(task)
					self.mainwindow.ui.microphoneImage.setEnabled(False)
				except:
					task = listen()
				return task

		def say(text):
			voice.say(text)
			voice.runAndWait()

		def encode(data, task):
			isException = False
			for allExceptions in exceptions:
				for exception in exceptions[allExceptions]:
					if exception in task:
						isException = True
						break
				break

			if not isException:
				for allCommands in data:
					for command in allCommands:
						if command in task:
							for comFor in data[allCommands]:
								for detailedCom in data[allCommands][comFor]:
									if detailedCom in task:
										sendCommand(allCommands[0], comFor)
										break
							break
			else:
				for allExceptions in exceptions:
					for exception in exceptions[allExceptions]:
						if exception in task:
							sendCommand(allExceptions, task)

		def sendCommand(command, thing):
			print("Command: ",command, "To: ", thing)
			if command == "включить":
				if thing == "свет":
					if (self.mainwindow.light1.isEnabled()):
						self.mainwindow.light1.setChecked(True)
						say("Свет включен.")
					else:
						say("Вы не подключены к Arduino.")
				elif thing == "вентилятор":
					if (self.mainwindow.fan.isEnabled()):
						self.mainwindow.fan.setChecked(True)
						say("Вентилятор включен.")
					else:
						say("Вы не подключены к Arduino.")
				elif thing == "всё":
					sendCommand("включить", "свет")
					sendCommand("включить", "вентилятор")
					say("Все подключенные устройства были включены.")
			elif command == "выключить":
				if thing == "свет":
					if (self.mainwindow.light1.isEnabled()):
						self.mainwindow.light1.setChecked(False)
						say("Свет выключен.")
					else:
						say("Вы не подключены к Arduino.")
				elif thing == "вентилятор":
					if (self.mainwindow.fan.isEnabled()):
						self.mainwindow.fan.setChecked(False)
						say("Вентилятор выключен.")
					else:
						say("Вы не подключены к Arduino.")
				elif thing == "всё":
					sendCommand("выключить", "свет")
					sendCommand("выключить", "вентилятор")
					say("Все подключенные устройства были выключены.")

			elif command == "открыть":
				if thing == "youtube":
					webbrowser.get(using='Chrome').open_new_tab("https://youtube.com")
					say("Открываю youtube.")
				elif thing == "блокнот":
					os.startfile('C:/Windows/system32/notepad.exe')
					say("Открываю блокнот.")
				elif thing == "калькулятор":
					os.startfile('C:/Windows/system32/calc.exe')
					say("Открываю калькулятор.")
				elif thing == "google":
					webbrowser.get(using='Chrome').open_new_tab("https://google.com")
					say("Открываю google.")
				elif thing == "яндекс":
					webbrowser.get(using='Chrome').open_new_tab("https://yandex.com")
					say("Открываю яндекс, но google - лучше.")
				elif thing == "вк":
					webbrowser.get(using='Chrome').open_new_tab("https://vk.com")
					say("Открываю ВКонтакте.")
				elif thing == "одноклассники":
					say("Какие одноклассники... Я был лучшего мнения о тебе.")
			if command == 'посчитай':
				m = ''
				for item in thing:
					if item == 'x' or item == '1' or item == '2' or item == '3' or item == '4' or item == '5' or item == '6' or item == '7' or item == '8' or item == '8' or item == '9' or item == '0' or item == '+' or item == '-' or item == '*' or item == '/':
						if item == 'x': m += '*'
						else: m += item
				print(m)
				res = eval(m)
				if res % 1 == 0:
					res = int(res)
				say('Ответ: ' + str(res))

		while True:
			encode(commands, listen())