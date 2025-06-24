import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import google.generativeai as genai
from dotenv import load_dotenv
import os
import spoty
import time
import csv
from datetime import datetime

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
        if hasattr(response, '_error') and response._error:
            return f"Error de Gemini: {response._error}"
        return response.text
    except Exception as e:
        return f"Ocurrió un error: {str(e)}"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        rec = ""
        try:
            rec = r.recognize_google(audio, language='es-ES').lower()
            rec_normalizado = rec.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
            if name in rec_normalizado:
                rec = rec_normalizado.replace(f"{name} ", "")
            else:
                print(f"Debes decir el nombre '{name}' para activar.")
                rec = ""
        except sr.UnknownValueError:
            print("No entendí lo que dijiste. Intenta de nuevo.")
            rec = ""
        except sr.RequestError as e:
            print(f"Error de conexión con el servicio de reconocimiento: {e}")
            rec = ""
        except Exception as e:
            print(f"Error inesperado al reconocer audio: {e}")
            rec = ""
    time.sleep(1)
    return rec

def guardar_historial(comando, respuesta):
    with open('historial_comandos.csv', mode='a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().isoformat(), comando, respuesta])

def run():
    modelo_gemini = configurar_gemini()

    while True:
        rec = get_audio()

        if not rec:
            continue

        if 'reproduce' in rec:
            if 'spotify' in rec:
                music = rec.replace('reproduce en spotify', '')
                speak(f'Reproduciendo {music}')
                spoty.play(os.getenv("spoty_client_id"), os.getenv("spoty_client_secret"), music)
                guardar_historial(rec, f'Reproduciendo {music} en Spotify')
            else:
                music = rec.replace('reproduce','')
                speak('Reproduciendo '+music)
                pywhatkit.playonyt(music)
                guardar_historial(rec, f'Reproduciendo {music} en YouTube')
        elif "hora" in rec:
            hora = datetime.now().strftime('%I:%M %p')
            speak('Son las '+hora)
            guardar_historial(rec, f'Son las {hora}')
        elif 'descansa' in rec:
            speak("Bye bye")
            guardar_historial(rec, 'Bye bye')
            break
        else:
            respuesta = chat_con_gemini(rec, modelo_gemini)
            speak(respuesta)
            guardar_historial(rec, respuesta)

if __name__ == "__main__":
    run()