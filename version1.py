import speech_recognition as sr
import pyttsx3

listener = sr.Recognizer()

engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

try:
    with sr.Microphone() as source:
        print("Escuchando...")
        listener.adjust_for_ambient_noise(source)
        voice = listener.listen(source)
        rec = listener.recognize_google(voice, language="es-ES")
        talk(rec)
except:
    pass