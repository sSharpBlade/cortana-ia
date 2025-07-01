import speech_recognition as sr
import pyttsx3
import time

def speak(text):
    """Función para que el asistente hable"""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

def listen_for_angie():
    """Escuchar específicamente para el nombre 'Angie'"""
    r = sr.Recognizer()
    
    print("🎤 Sistema de prueba de activación por voz")
    print("📝 Di 'Asistente' seguido de un comando para activar")
    print("🔴 Presiona Ctrl+C para salir")
    print("-" * 50)
    
    while True:
        try:
            with sr.Microphone() as source:
                print("👂 Escuchando... (di 'Asistente' para activar)")
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=3, phrase_time_limit=5)
                
                try:
                    # Reconocer el audio
                    rec = r.recognize_google(audio, language='es-ES').lower()
                    print(f"🎯 Reconocido: '{rec}'")
                    
                    # Normalizar texto (quitar acentos)
                    rec_normalizado = rec.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
                    
                    # Verificar si dice "asistente"
                    if "asistente" in rec_normalizado:
                        print("✅ ¡Asistente detectado! Procesando comando...")
                        
                        # Extraer el comando después de "asistente"
                        command = rec_normalizado.replace("asistente", "").strip()
                        print(f"📋 Comando: '{command}'")
                        
                        # Procesar comandos básicos
                        if "hora" in command:
                            import datetime
                            hora = datetime.datetime.now().strftime('%I:%M %p')
                            response = f"Son las {hora}"
                            print(f"⏰ {response}")
                            speak(response)
                            
                        elif "hola" in command or "buenos días" in command:
                            response = "¡Hola! ¿En qué puedo ayudarte?"
                            print(f"👋 {response}")
                            speak(response)
                            
                        elif "adiós" in command or "bye" in command or "descansa" in command:
                            response = "¡Hasta luego! Que tengas un buen día"
                            print(f"👋 {response}")
                            speak(response)
                            break
                            
                        else:
                            response = f"Entendí tu comando: {command}. Esta es una versión de prueba."
                            print(f"🤖 {response}")
                            speak(response)
                            
                    else:
                        print("❌ No se detectó 'Asistente'. Di 'Asistente' para activar el asistente.")
                        
                except sr.UnknownValueError:
                    print("❓ No pude entender lo que dijiste")
                except sr.RequestError as e:
                    print(f"❌ Error de conexión: {e}")
                    
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    print("🚀 Iniciando prueba de activación por voz...")
    speak("Hola, soy tu Asistente. Estoy lista para ayudarte. Di mi nombre para activarme.")
    listen_for_angie() 