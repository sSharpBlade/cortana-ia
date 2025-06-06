import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

name = 'alexa'

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def configurar_gemini():
    genai.configure(api_key=GEMINI_API_KEY)
    
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 20,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    model = genai.GenerativeModel('gemini-2.0-flash-001',
                                generation_config=generation_config,
                                safety_settings=safety_settings)
    return model

def chat_con_gemini(pregunta, model):
    try:
        response = model.generate_content(pregunta)
        if response._error:
            return f"Error de Gemini: {response._error}"
        return response.text
    except Exception as e:
        return f"Ocurrió un error: {str(e)}"

def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    rec = ""
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            voice = listener.listen(source)
            rec = listener.recognize_google(voice, language="es-ES")
            rec = rec.lower()
            if name in rec:
                rec = rec.replace(name, '')
                print(rec)
    except Exception as e:
        print(f"Error en listen: {e}")
    return rec

def run():
    modelo_gemini = configurar_gemini()

    while True:
        rec = listen()
        if not rec:
            continue

        if 'reproduce' in rec:
            music = rec.replace('reproduce','')
            talk('Reproduciendo '+music)
            pywhatkit.playonyt(music)
        elif "hora" in rec:
            hora = datetime.datetime.now().strftime('%I:%M %p')
            talk('Son las '+hora)
        else:
            respuesta = chat_con_gemini(rec, modelo_gemini)
            talk(respuesta)

if __name__ == "__main__":
    run()