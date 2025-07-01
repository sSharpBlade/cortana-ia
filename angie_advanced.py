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
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import requests
import wikipedia
import json
import pyautogui
from PIL import Image, ImageTk
import customtkinter as ctk
import subprocess
import platform
import psutil
import webbrowser
import sqlite3
import schedule

# Configurar CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
DEFAULT_CITY = os.getenv("DEFAULT_CITY", "Madrid")

class AngieAdvanced:
    def __init__(self):
        self.name = 'asistente'
        self.is_listening = False
        self.is_running = False
        self.reminders = []
        self.tasks = []
        
        # Configurar reconocimiento de voz
        self.listener = sr.Recognizer()
        
        # Configurar síntesis de voz
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)
        self.engine.setProperty('rate', 150)
        
        # Configurar Gemini
        self.modelo_gemini = self.configurar_gemini()
        
        # Configurar base de datos
        self.setup_database()
        
        # Crear interfaz
        self.create_gui()
        
        # Iniciar scheduler para recordatorios
        self.start_scheduler()
        
    def setup_database(self):
        """Configurar base de datos SQLite para recordatorios y tareas"""
        self.conn = sqlite3.connect('angie_data.db')
        self.cursor = self.conn.cursor()
        
        # Crear tablas
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                datetime TEXT NOT NULL,
                completed BOOLEAN DEFAULT 0
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                priority TEXT DEFAULT 'medium',
                completed BOOLEAN DEFAULT 0,
                created_date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        
    def configurar_gemini(self):
        genai.configure(api_key=GEMINI_API_KEY)
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 1000,
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

    def create_gui(self):
        self.root = ctk.CTk()
        self.root.title("Angie Advanced - Asistente Virtual Pro")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(main_frame, text="🎤 Angie Advanced - Tu Asistente Virtual Pro", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=20)
        
        # Frame para controles principales
        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(fill="x", padx=20, pady=10)
        
        # Botón de activar/desactivar
        self.toggle_button = ctk.CTkButton(controls_frame, text="🎤 Activar Angie", 
                                          command=self.toggle_listening,
                                          font=ctk.CTkFont(size=16))
        self.toggle_button.pack(pady=10)
        
        # Estado del asistente
        self.status_label = ctk.CTkLabel(controls_frame, text="Estado: Desactivado", 
                                        font=ctk.CTkFont(size=14))
        self.status_label.pack(pady=5)
        
        # Frame para comandos rápidos
        quick_commands_frame = ctk.CTkFrame(main_frame)
        quick_commands_frame.pack(fill="x", padx=20, pady=10)
        
        quick_label = ctk.CTkLabel(quick_commands_frame, text="Comandos Rápidos:", 
                                  font=ctk.CTkFont(size=16, weight="bold"))
        quick_label.pack(pady=10)
        
        # Botones de comandos rápidos
        commands_frame = ctk.CTkFrame(quick_commands_frame)
        commands_frame.pack(pady=10)
        
        commands = [
            ("🌤️ Clima", self.get_weather),
            ("📰 Noticias", self.get_news),
            ("⏰ Hora", self.get_time),
            ("🔍 Buscar", self.search_wikipedia),
            ("📝 Notas", self.take_notes),
            ("🖥️ Captura", self.take_screenshot),
            ("💻 Sistema", self.system_info),
            ("📅 Recordatorios", self.show_reminders),
            ("✅ Tareas", self.show_tasks),
            ("🌐 Navegar", self.open_website)
        ]
        
        for i, (text, command) in enumerate(commands):
            btn = ctk.CTkButton(commands_frame, text=text, command=command, width=120)
            btn.grid(row=i//5, column=i%5, padx=5, pady=5)
        
        # Frame para entrada de texto
        text_frame = ctk.CTkFrame(main_frame)
        text_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Entrada de texto
        self.text_input = ctk.CTkEntry(text_frame, placeholder_text="Escribe tu comando aquí...", 
                                      font=ctk.CTkFont(size=14))
        self.text_input.pack(fill="x", padx=10, pady=10)
        self.text_input.bind("<Return>", self.send_text_command)
        
        # Botón enviar
        send_button = ctk.CTkButton(text_frame, text="Enviar", command=self.send_text_command)
        send_button.pack(pady=5)
        
        # Área de chat
        chat_frame = ctk.CTkFrame(main_frame)
        chat_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        chat_label = ctk.CTkLabel(chat_frame, text="Conversación:", 
                                 font=ctk.CTkFont(size=16, weight="bold"))
        chat_label.pack(pady=10)
        
        # Área de texto para mostrar conversación
        self.chat_area = ctk.CTkTextbox(chat_frame, font=ctk.CTkFont(size=12))
        self.chat_area.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame para información del sistema
        info_frame = ctk.CTkFrame(main_frame)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        self.info_label = ctk.CTkLabel(info_frame, text="Listo para ayudarte", 
                                      font=ctk.CTkFont(size=12))
        self.info_label.pack(pady=5)
        
        # Configurar cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def start_scheduler(self):
        """Iniciar el scheduler para recordatorios"""
        def run_scheduler():
            while self.is_running:
                schedule.run_pending()
                time.sleep(1)
        
        self.scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
    def toggle_listening(self):
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening()
    
    def start_listening(self):
        self.is_listening = True
        self.is_running = True
        self.toggle_button.configure(text="🔴 Detener Angie")
        self.status_label.configure(text="Estado: Escuchando...")
        self.info_label.configure(text="Di 'Angie' seguido de tu comando")
        
        # Iniciar hilo de escucha
        self.listen_thread = threading.Thread(target=self.listen_loop)
        self.listen_thread.daemon = True
        self.listen_thread.start()
    
    def stop_listening(self):
        self.is_listening = False
        self.is_running = False
        self.toggle_button.configure(text="🎤 Activar Angie")
        self.status_label.configure(text="Estado: Desactivado")
        self.info_label.configure(text="Asistente detenido")
    
    def listen_loop(self):
        while self.is_listening and self.is_running:
            try:
                with sr.Microphone() as source:
                    self.listener.adjust_for_ambient_noise(source, duration=0.5)
                    try:
                        audio = self.listener.listen(source, timeout=7, phrase_time_limit=8)
                        rec = self.listener.recognize_google(audio, language='es-ES').lower()
                        rec_normalizado = rec.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
                        if self.name in rec_normalizado:
                            rec = rec_normalizado.replace(f"{self.name} ", "")
                            self.process_command(rec)
                        else:
                            self.update_info(f"Di '{self.name.capitalize()}' para activar el asistente")
                    except sr.WaitTimeoutError:
                        self.update_info("No se detectó voz, esperando de nuevo...")
                        continue
                    except sr.UnknownValueError:
                        self.update_info("No entendí lo que dijiste. Intenta de nuevo.")
                        continue
                    except sr.RequestError as e:
                        self.update_info(f"Error de conexión: {e}")
                        continue
            except Exception as e:
                if self.is_listening:
                    self.update_info(f"Error: {e}")
                time.sleep(1)
                continue
    
    def process_command(self, command):
        self.add_to_chat(f"Tú: {command}")
        
        # Comandos de música
        if 'reproduce' in command:
            if 'spotify' in command:
                music = command.replace('reproduce en spotify', '').strip()
                self.speak(f'Reproduciendo {music} en Spotify')
                self.add_to_chat(f"Angie: Reproduciendo {music} en Spotify")
                try:
                    spoty.play(os.getenv("spoty_client_id"), os.getenv("spoty_client_secret"), music)
                except:
                    self.add_to_chat("Angie: Error al reproducir en Spotify")
            else:
                music = command.replace('reproduce', '').strip()
                self.speak(f'Reproduciendo {music}')
                self.add_to_chat(f"Angie: Reproduciendo {music} en YouTube")
                try:
                    pywhatkit.playonyt(music)
                except:
                    self.add_to_chat("Angie: Error al reproducir en YouTube")
        
        # Comandos de tiempo
        elif "hora" in command:
            hora = datetime.now().strftime('%I:%M %p')
            self.speak(f'Son las {hora}')
            self.add_to_chat(f"Angie: Son las {hora}")
        
        # Comandos de clima
        elif "clima" in command or "tiempo" in command:
            # Extraer ciudad si se especifica
            if " en " in command:
                city = command.split(" en ")[-1].strip()
                self.get_weather_for_city(city)
            elif " de " in command:
                city = command.split(" de ")[-1].strip()
                self.get_weather_for_city(city)
            else:
                self.get_weather()
        
        # Comandos de noticias
        elif "noticias" in command:
            self.get_news()
        
        # Comandos de búsqueda
        elif "busca" in command or "buscar" in command:
            query = command.replace("busca", "").replace("buscar", "").strip()
            self.search_wikipedia(query)
        
        # Comandos de notas
        elif "nota" in command or "anota" in command:
            self.take_notes()
        
        # Comandos de captura
        elif "captura" in command or "screenshot" in command:
            self.take_screenshot()
        
        # Comandos de sistema
        elif "sistema" in command or "computadora" in command:
            self.system_info()
        
        # Comandos de recordatorios
        elif "recordatorio" in command or "recordar" in command:
            self.add_reminder(command)
        
        # Comandos de tareas
        elif "tarea" in command or "agregar tarea" in command:
            self.add_task(command)
        
        # Comandos de navegación
        elif "abre" in command or "navega" in command:
            self.open_website(command)
        
        # Comandos de cierre
        elif "descansa" in command or "adiós" in command or "bye" in command:
            self.speak("¡Hasta luego! Que tengas un buen día")
            self.add_to_chat("Angie: ¡Hasta luego! Que tengas un buen día")
            self.stop_listening()
        
        else:
            # Usar Gemini para respuestas generales
            respuesta = self.chat_with_gemini(command)
            self.speak(respuesta)
            self.add_to_chat(f"Angie: {respuesta}")
        
        self.guardar_historial(command, "Comando procesado")
    
    def chat_with_gemini(self, pregunta):
        try:
            response = self.modelo_gemini.generate_content(pregunta)
            if hasattr(response, '_error') and response._error:
                return f"Error de Gemini: {response._error}"
            return response.text
        except Exception as e:
            return f"Ocurrió un error: {str(e)}"
    
    def speak(self, text):
        def speak_thread():
            self.engine.say(text)
            self.engine.runAndWait()
        
        threading.Thread(target=speak_thread, daemon=True).start()
    
    def add_to_chat(self, message):
        self.chat_area.insert("end", message + "\n")
        self.chat_area.see("end")
    
    def update_info(self, message):
        self.info_label.configure(text=message)
    
    def send_text_command(self, event=None):
        command = self.text_input.get().strip()
        if command:
            self.text_input.delete(0, "end")
            self.process_command(command)
    
    def get_weather(self):
        try:
            city = DEFAULT_CITY
            # WeatherAPI endpoint for current weather
            url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&lang=es"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                temp = data['current']['temp_c']
                condition = data['current']['condition']['text']
                humidity = data['current']['humidity']
                wind_speed = data['current']['wind_kph']
                feels_like = data['current']['feelslike_c']
                
                weather_info = f"En {city}: {temp}°C, {condition}. Sensación térmica: {feels_like}°C, humedad: {humidity}%, viento: {wind_speed} km/h"
                self.speak(weather_info)
                self.add_to_chat(f"Angie: {weather_info}")
            else:
                error_msg = data.get('error', {}).get('message', 'Error desconocido')
                self.add_to_chat(f"Angie: No pude obtener el clima: {error_msg}")
        except Exception as e:
            self.add_to_chat(f"Angie: Error al obtener el clima: {str(e)}")
    
    def get_weather_for_city(self, city):
        """Obtiene el clima para una ciudad específica"""
        try:
            # WeatherAPI endpoint for current weather
            url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&lang=es"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                temp = data['current']['temp_c']
                condition = data['current']['condition']['text']
                humidity = data['current']['humidity']
                wind_speed = data['current']['wind_kph']
                feels_like = data['current']['feelslike_c']
                location = data['location']['name']
                country = data['location']['country']
                
                weather_info = f"En {location}, {country}: {temp}°C, {condition}. Sensación térmica: {feels_like}°C, humedad: {humidity}%, viento: {wind_speed} km/h"
                self.speak(weather_info)
                self.add_to_chat(f"Angie: {weather_info}")
            else:
                error_msg = data.get('error', {}).get('message', 'Ciudad no encontrada')
                self.add_to_chat(f"Angie: No pude obtener el clima de {city}: {error_msg}")
        except Exception as e:
            self.add_to_chat(f"Angie: Error al obtener el clima de {city}: {str(e)}")
    
    def get_news(self):
        try:
            url = f"https://newsapi.org/v2/top-headlines?country=es&apiKey={NEWS_API_KEY}"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200 and data['articles']:
                news = data['articles'][0]
                title = news['title']
                self.speak(f"Noticia principal: {title}")
                self.add_to_chat(f"Angie: Noticia principal: {title}")
                self.add_to_chat(f"Angie: {news.get('description', 'Sin descripción')}")
            else:
                self.add_to_chat("Angie: No pude obtener las noticias")
        except:
            self.add_to_chat("Angie: Error al obtener las noticias")
    
    def get_time(self):
        hora = datetime.now().strftime('%I:%M %p')
        fecha = datetime.now().strftime('%d/%m/%Y')
        self.speak(f'Son las {hora} del {fecha}')
        self.add_to_chat(f"Angie: Son las {hora} del {fecha}")
    
    def search_wikipedia(self, query=""):
        try:
            if not query:
                query = "Python programming"
            
            search_results = wikipedia.search(query, results=1)
            if search_results:
                page = wikipedia.page(search_results[0])
                summary = wikipedia.summary(search_results[0], sentences=2)
                self.speak(f"Encontré información sobre {query}: {summary}")
                self.add_to_chat(f"Angie: {summary}")
            else:
                self.add_to_chat("Angie: No encontré información sobre eso")
        except:
            self.add_to_chat("Angie: Error al buscar en Wikipedia")
    
    def take_notes(self):
        try:
            note_window = ctk.CTkToplevel(self.root)
            note_window.title("Tomar Notas")
            note_window.geometry("400x300")
            
            note_text = ctk.CTkTextbox(note_window)
            note_text.pack(fill="both", expand=True, padx=10, pady=10)
            
            def save_note():
                note_content = note_text.get("1.0", "end-1c")
                if note_content.strip():
                    with open(f"nota_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", "w", encoding="utf-8") as f:
                        f.write(note_content)
                    messagebox.showinfo("Nota Guardada", "Nota guardada exitosamente")
                    note_window.destroy()
            
            save_button = ctk.CTkButton(note_window, text="Guardar Nota", command=save_note)
            save_button.pack(pady=10)
            
            self.add_to_chat("Angie: Ventana de notas abierta")
        except:
            self.add_to_chat("Angie: Error al abrir las notas")
    
    def take_screenshot(self):
        try:
            screenshot = pyautogui.screenshot()
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            screenshot.save(filename)
            self.speak("Captura de pantalla guardada")
            self.add_to_chat(f"Angie: Captura de pantalla guardada como {filename}")
        except:
            self.add_to_chat("Angie: Error al tomar la captura de pantalla")
    
    def system_info(self):
        try:
            # Información del sistema
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            system_info = f"Sistema: CPU {cpu_percent}%, RAM {memory.percent}%, Disco {disk.percent}%"
            self.speak(system_info)
            self.add_to_chat(f"Angie: {system_info}")
        except:
            self.add_to_chat("Angie: Error al obtener información del sistema")
    
    def add_reminder(self, command):
        try:
            # Extraer información del recordatorio del comando
            reminder_text = command.replace("recordatorio", "").replace("recordar", "").strip()
            
            # Crear ventana para configurar recordatorio
            reminder_window = ctk.CTkToplevel(self.root)
            reminder_window.title("Agregar Recordatorio")
            reminder_window.geometry("400x300")
            
            ctk.CTkLabel(reminder_window, text="Título:").pack(pady=5)
            title_entry = ctk.CTkEntry(reminder_window, width=300)
            title_entry.pack(pady=5)
            title_entry.insert(0, reminder_text)
            
            ctk.CTkLabel(reminder_window, text="Fecha y hora (YYYY-MM-DD HH:MM):").pack(pady=5)
            datetime_entry = ctk.CTkEntry(reminder_window, width=300)
            datetime_entry.pack(pady=5)
            datetime_entry.insert(0, (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M"))
            
            def save_reminder():
                title = title_entry.get()
                datetime_str = datetime_entry.get()
                
                if title and datetime_str:
                    try:
                        reminder_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
                        
                        # Guardar en base de datos
                        self.cursor.execute("INSERT INTO reminders (title, datetime) VALUES (?, ?)", 
                                          (title, reminder_datetime.isoformat()))
                        self.conn.commit()
                        
                        # Programar recordatorio
                        schedule.every().day.at(reminder_datetime.strftime("%H:%M")).do(
                            self.trigger_reminder, title
                        )
                        
                        messagebox.showinfo("Recordatorio", f"Recordatorio '{title}' programado para {datetime_str}")
                        reminder_window.destroy()
                        
                    except ValueError:
                        messagebox.showerror("Error", "Formato de fecha inválido")
            
            save_button = ctk.CTkButton(reminder_window, text="Guardar Recordatorio", command=save_reminder)
            save_button.pack(pady=20)
            
        except Exception as e:
            self.add_to_chat(f"Angie: Error al crear recordatorio: {e}")
    
    def trigger_reminder(self, title):
        """Activar recordatorio"""
        self.speak(f"Recordatorio: {title}")
        self.add_to_chat(f"Angie: 🔔 Recordatorio: {title}")
        messagebox.showinfo("Recordatorio", f"🔔 {title}")
    
    def show_reminders(self):
        try:
            self.cursor.execute("SELECT * FROM reminders WHERE completed = 0 ORDER BY datetime")
            reminders = self.cursor.fetchall()
            
            if reminders:
                reminder_text = "Recordatorios pendientes:\n"
                for reminder in reminders:
                    reminder_text += f"• {reminder[1]} - {reminder[2]}\n"
                self.add_to_chat(f"Angie: {reminder_text}")
            else:
                self.add_to_chat("Angie: No hay recordatorios pendientes")
        except:
            self.add_to_chat("Angie: Error al mostrar recordatorios")
    
    def add_task(self, command):
        try:
            task_text = command.replace("tarea", "").replace("agregar tarea", "").strip()
            
            task_window = ctk.CTkToplevel(self.root)
            task_window.title("Agregar Tarea")
            task_window.geometry("400x250")
            
            ctk.CTkLabel(task_window, text="Tarea:").pack(pady=5)
            task_entry = ctk.CTkEntry(task_window, width=300)
            task_entry.pack(pady=5)
            task_entry.insert(0, task_text)
            
            ctk.CTkLabel(task_window, text="Prioridad:").pack(pady=5)
            priority_var = ctk.StringVar(value="medium")
            priority_frame = ctk.CTkFrame(task_window)
            priority_frame.pack(pady=5)
            
            ctk.CTkRadioButton(priority_frame, text="Baja", variable=priority_var, value="low").pack(side="left", padx=10)
            ctk.CTkRadioButton(priority_frame, text="Media", variable=priority_var, value="medium").pack(side="left", padx=10)
            ctk.CTkRadioButton(priority_frame, text="Alta", variable=priority_var, value="high").pack(side="left", padx=10)
            
            def save_task():
                task = task_entry.get()
                priority = priority_var.get()
                
                if task:
                    self.cursor.execute("INSERT INTO tasks (title, priority) VALUES (?, ?)", (task, priority))
                    self.conn.commit()
                    messagebox.showinfo("Tarea", f"Tarea '{task}' agregada con prioridad {priority}")
                    task_window.destroy()
            
            save_button = ctk.CTkButton(task_window, text="Guardar Tarea", command=save_task)
            save_button.pack(pady=20)
            
        except Exception as e:
            self.add_to_chat(f"Angie: Error al crear tarea: {e}")
    
    def show_tasks(self):
        try:
            self.cursor.execute("SELECT * FROM tasks WHERE completed = 0 ORDER BY priority DESC, created_date")
            tasks = self.cursor.fetchall()
            
            if tasks:
                task_text = "Tareas pendientes:\n"
                for task in tasks:
                    priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                    task_text += f"• {priority_emoji.get(task[2], '⚪')} {task[1]}\n"
                self.add_to_chat(f"Angie: {task_text}")
            else:
                self.add_to_chat("Angie: No hay tareas pendientes")
        except:
            self.add_to_chat("Angie: Error al mostrar tareas")
    
    def open_website(self, command):
        try:
            # Extraer URL del comando
            if "abre" in command:
                url = command.replace("abre", "").strip()
            elif "navega" in command:
                url = command.replace("navega", "").strip()
            else:
                url = command
            
            # Agregar https si no está presente
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            webbrowser.open(url)
            self.speak(f"Abriendo {url}")
            self.add_to_chat(f"Angie: Abriendo {url}")
        except:
            self.add_to_chat("Angie: Error al abrir el sitio web")
    
    def guardar_historial(self, comando, respuesta):
        try:
            with open('historial_comandos.csv', mode='a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([datetime.now().isoformat(), comando, respuesta])
        except:
            pass
    
    def on_closing(self):
        self.stop_listening()
        if hasattr(self, 'conn'):
            self.conn.close()
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AngieAdvanced()
    app.run()