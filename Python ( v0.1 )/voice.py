import pyttsx3

voice = pyttsx3.init()


def say(self, text):
    voice.say(text)
    voice.runAndWait()
    voice.endLoop()
    voice.stop()