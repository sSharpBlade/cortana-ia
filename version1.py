import speech_recognition as sr

listener = sr.Recognizer()

try:
    with sr.Microphone() as source:
        print("Escuchando...")
        listener.adjust_for_ambient_noise(source)
        voice = listener.listen(source)
        rec = listener.recognize_google(voice, language="es-ES")
        print(rec)
except:
    pass