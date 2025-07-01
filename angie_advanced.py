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
        
        # Crear tabla para notas
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_date TEXT DEFAULT CURRENT_TIMESTAMP,
                modified_date TEXT DEFAULT CURRENT_TIMESTAMP
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
            ("📝 Nueva Nota", self.take_notes),
            ("📚 Ver Notas", self.show_all_notes),
            ("🖥️ Captura", self.take_screenshot),
            ("💻 Sistema", self.system_info),
            ("📅 Recordatorios", self.show_reminders),
            ("✅ Tareas", self.show_tasks)
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
        elif "noticias" in command or "noticia" in command:
            # Detectar categoría específica
            if "deportes" in command or "deporte" in command:
                self.get_quick_news_summary("sports")
            elif "tecnología" in command or "tecnologia" in command:
                self.get_quick_news_summary("technology")
            elif "ciencia" in command:
                self.get_quick_news_summary("science")
            elif "salud" in command:
                self.get_quick_news_summary("health")
            elif "negocios" in command or "economía" in command or "economia" in command:
                self.get_quick_news_summary("business")
            elif "entretenimiento" in command:
                self.get_quick_news_summary("entertainment")
            else:
                # Si no se especifica categoría, mostrar ventana completa
                if "rápidas" in command or "rapidas" in command or "resumen" in command:
                    self.get_quick_news_summary("general")
                else:
                    self.get_news()
        
        # Comandos de búsqueda
        elif "busca" in command or "buscar" in command:
            query = command.replace("busca", "").replace("buscar", "").strip()
            if query:
                self.search_wikipedia(query)
            else:
                self.speak("¿Qué quieres que busque?")
                self.add_to_chat("Angie: ¿Qué quieres que busque en Wikipedia?")
                self.show_search_window()
        
        # Comandos de notas
        elif "crear nota" in command or "nueva nota" in command or "tomar nota" in command or "anota" in command:
            self.take_notes()
        
        elif "ver notas" in command or "mostrar notas" in command or "mis notas" in command:
            self.show_all_notes()
        
        elif "buscar nota" in command:
            # Extraer término de búsqueda
            search_term = command.replace("buscar nota", "").replace("buscar en notas", "").strip()
            if search_term:
                self.search_notes_by_voice_command(search_term)
            else:
                self.speak("¿Qué quieres buscar en las notas?")
                self.add_to_chat("Angie: ¿Qué quieres buscar en las notas?")
        
        elif "cuántas notas" in command or "resumen de notas" in command:
            self.get_notes_summary()
        
        elif "leer notas" in command:
            self.read_recent_notes_aloud()
        
        # Comandos de notas específicas (legacy - crear nota simple)
        elif "nota" in command:
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
        
        elif "ayuda notas" in command or "ayuda de notas" in command:
            self.show_notes_help()
        
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
    
    def get_news(self, category="general", query="", country="es"):
        """Obtener noticias con opciones avanzadas"""
        self.show_news_window(category, query, country)
    
    def get_time(self):
        hora = datetime.now().strftime('%I:%M %p')
        fecha = datetime.now().strftime('%d/%m/%Y')
        self.speak(f'Son las {hora} del {fecha}')
        self.add_to_chat(f"Angie: Son las {hora} del {fecha}")
    
    def search_wikipedia(self, query=""):
        """Buscar información en Wikipedia"""
        try:
            if not query:
                # Si no hay query, abrir ventana para ingresar búsqueda
                self.show_search_window()
                return
            
            # Configurar idioma español para Wikipedia
            wikipedia.set_lang("es")
            
            self.add_to_chat(f"Angie: 🔍 Buscando '{query}' en Wikipedia...")
            
            search_results = wikipedia.search(query, results=3)
            if search_results:
                try:
                    # Intentar obtener el primer resultado
                    page = wikipedia.page(search_results[0])
                    summary = wikipedia.summary(search_results[0], sentences=3)
                    
                    response = f"Encontré información sobre '{query}': {summary}"
                    self.speak(response)
                    self.add_to_chat(f"Angie: 📖 {response}")
                    
                    # Mostrar enlace para más información
                    self.add_to_chat(f"Angie: 🔗 Más información: {page.url}")
                    
                except wikipedia.exceptions.DisambiguationError as e:
                    # Si hay ambigüedad, mostrar opciones
                    options = e.options[:5]  # Máximo 5 opciones
                    options_text = ", ".join(options)
                    response = f"Encontré varias opciones para '{query}': {options_text}. Sé más específico."
                    self.speak(response)
                    self.add_to_chat(f"Angie: 📋 {response}")
                    
                except wikipedia.exceptions.PageError:
                    self.add_to_chat(f"Angie: ❌ No encontré una página específica para '{query}'")
                    
            else:
                response = f"No encontré resultados para '{query}' en Wikipedia"
                self.speak(response)
                self.add_to_chat(f"Angie: ❌ {response}")
                
        except Exception as e:
            error_msg = f"Error al buscar '{query}' en Wikipedia: {str(e)}"
            self.add_to_chat(f"Angie: ❌ {error_msg}")
    
    def show_search_window(self):
        """Mostrar ventana para ingresar término de búsqueda"""
        try:
            search_window = ctk.CTkToplevel(self.root)
            search_window.title("Buscar en Wikipedia")
            search_window.geometry("400x200")
            search_window.grab_set()  # Hacer la ventana modal
            
            # Título
            title_label = ctk.CTkLabel(search_window, text="🔍 Buscar en Wikipedia", 
                                      font=ctk.CTkFont(size=18, weight="bold"))
            title_label.pack(pady=20)
            
            # Campo de búsqueda
            search_label = ctk.CTkLabel(search_window, text="¿Qué quieres buscar?")
            search_label.pack(pady=5)
            
            search_entry = ctk.CTkEntry(search_window, width=300, 
                                       placeholder_text="Ejemplo: inteligencia artificial")
            search_entry.pack(pady=10)
            search_entry.focus_set()  # Enfocar el campo de entrada
            
            def perform_search():
                query = search_entry.get().strip()
                if query:
                    search_window.destroy()
                    self.search_wikipedia(query)
                else:
                    search_entry.configure(placeholder_text="Por favor, ingresa un término de búsqueda")
            
            def on_enter(event):
                perform_search()
            
            # Vincular Enter para buscar
            search_entry.bind("<Return>", on_enter)
            
            # Botones
            button_frame = ctk.CTkFrame(search_window)
            button_frame.pack(pady=20)
            
            search_button = ctk.CTkButton(button_frame, text="🔍 Buscar", 
                                         command=perform_search)
            search_button.pack(side="left", padx=5)
            
            cancel_button = ctk.CTkButton(button_frame, text="Cancelar", 
                                         command=search_window.destroy)
            cancel_button.pack(side="left", padx=5)
            
            self.add_to_chat("Angie: Ventana de búsqueda abierta")
            
        except Exception as e:
            self.add_to_chat(f"Angie: Error al abrir ventana de búsqueda: {str(e)}")
    
    def take_notes(self):
        """Abrir ventana para crear una nueva nota"""
        try:
            note_window = ctk.CTkToplevel(self.root)
            note_window.title("Crear Nueva Nota")
            note_window.geometry("500x400")
            
            # Campo para el título
            title_label = ctk.CTkLabel(note_window, text="Título:")
            title_label.pack(pady=(10, 5))
            
            title_entry = ctk.CTkEntry(note_window, width=400)
            title_entry.pack(pady=(0, 10))
            
            # Campo para el contenido
            content_label = ctk.CTkLabel(note_window, text="Contenido:")
            content_label.pack(pady=(0, 5))
            
            note_text = ctk.CTkTextbox(note_window, height=200)
            note_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
            
            def save_note():
                title = title_entry.get().strip()
                content = note_text.get("1.0", "end-1c").strip()
                
                if not title:
                    title = f"Nota {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                
                if content:
                    try:
                        cursor = self.conn.cursor()
                        cursor.execute('''
                            INSERT INTO notes (title, content, created_date, modified_date)
                            VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                        ''', (title, content))
                        self.conn.commit()
                        
                        messagebox.showinfo("Nota Guardada", "Nota guardada exitosamente en la base de datos")
                        self.speak("Nota guardada correctamente")
                        note_window.destroy()
                        self.add_to_chat(f"Angie: Nota '{title}' guardada exitosamente")
                    except Exception as e:
                        messagebox.showerror("Error", f"Error al guardar la nota: {str(e)}")
                        self.add_to_chat("Angie: Error al guardar la nota")
                else:
                    messagebox.showwarning("Advertencia", "El contenido de la nota no puede estar vacío")
            
            # Botones
            button_frame = ctk.CTkFrame(note_window)
            button_frame.pack(pady=10)
            
            save_button = ctk.CTkButton(button_frame, text="Guardar Nota", command=save_note)
            save_button.pack(side="left", padx=5)
            
            view_button = ctk.CTkButton(button_frame, text="Ver Todas las Notas", 
                                      command=self.show_all_notes)
            view_button.pack(side="left", padx=5)
            
            self.add_to_chat("Angie: Ventana para crear nota abierta")
        except Exception as e:
            self.add_to_chat(f"Angie: Error al abrir las notas: {str(e)}")
    
    def show_all_notes(self):
        """Mostrar todas las notas guardadas en una ventana"""
        try:
            notes_window = ctk.CTkToplevel(self.root)
            notes_window.title("Todas las Notas")
            notes_window.geometry("700x500")
            
            # Frame para la lista de notas
            notes_frame = ctk.CTkScrollableFrame(notes_window)
            notes_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Obtener todas las notas
            cursor = self.conn.cursor()
            cursor.execute('SELECT id, title, content, created_date, modified_date FROM notes ORDER BY modified_date DESC')
            notes = cursor.fetchall()
            
            if not notes:
                no_notes_label = ctk.CTkLabel(notes_frame, text="No hay notas guardadas")
                no_notes_label.pack(pady=50)
                return
            
            for note in notes:
                note_id, title, content, created_date, modified_date = note
                
                # Frame para cada nota
                note_frame = ctk.CTkFrame(notes_frame)
                note_frame.pack(fill="x", pady=5, padx=5)
                
                # Título de la nota
                title_label = ctk.CTkLabel(note_frame, text=f"📝 {title}", 
                                         font=ctk.CTkFont(size=16, weight="bold"))
                title_label.pack(anchor="w", padx=10, pady=(5, 0))
                
                # Fecha
                date_label = ctk.CTkLabel(note_frame, text=f"Creada: {created_date[:16]}")
                date_label.pack(anchor="w", padx=10)
                
                # Contenido (preview)
                preview = content[:100] + "..." if len(content) > 100 else content
                content_label = ctk.CTkLabel(note_frame, text=preview, wraplength=600)
                content_label.pack(anchor="w", padx=10, pady=(0, 5))
                
                # Botones
                button_frame = ctk.CTkFrame(note_frame)
                button_frame.pack(fill="x", padx=10, pady=5)
                
                read_button = ctk.CTkButton(button_frame, text="Leer", width=80,
                                          command=lambda n=note: self.read_note_aloud(n))
                read_button.pack(side="left", padx=2)
                
                edit_button = ctk.CTkButton(button_frame, text="Editar", width=80,
                                          command=lambda n=note: self.edit_note(n))
                edit_button.pack(side="left", padx=2)
                
                delete_button = ctk.CTkButton(button_frame, text="Eliminar", width=80,
                                            command=lambda n=note: self.delete_note(n, notes_window))
                delete_button.pack(side="left", padx=2)
                
                copy_button = ctk.CTkButton(button_frame, text="Copiar", width=80,
                                          command=lambda c=content: self.copy_to_clipboard(c))
                copy_button.pack(side="left", padx=2)
            
            self.add_to_chat(f"Angie: Mostrando {len(notes)} notas guardadas")
            
        except Exception as e:
            self.add_to_chat(f"Angie: Error al mostrar las notas: {str(e)}")
    
    def read_note_aloud(self, note):
        """Leer una nota en voz alta"""
        try:
            note_id, title, content, created_date, modified_date = note
            text_to_read = f"Nota: {title}. Contenido: {content}"
            self.speak(text_to_read)
            self.add_to_chat(f"Angie: Leyendo nota '{title}'")
        except Exception as e:
            self.add_to_chat(f"Angie: Error al leer la nota: {str(e)}")
    
    def edit_note(self, note):
        """Editar una nota existente"""
        try:
            note_id, title, content, created_date, modified_date = note
            
            edit_window = ctk.CTkToplevel(self.root)
            edit_window.title(f"Editar Nota - {title}")
            edit_window.geometry("500x400")
            
            # Campo para el título
            title_label = ctk.CTkLabel(edit_window, text="Título:")
            title_label.pack(pady=(10, 5))
            
            title_entry = ctk.CTkEntry(edit_window, width=400)
            title_entry.pack(pady=(0, 10))
            title_entry.insert(0, title)
            
            # Campo para el contenido
            content_label = ctk.CTkLabel(edit_window, text="Contenido:")
            content_label.pack(pady=(0, 5))
            
            note_text = ctk.CTkTextbox(edit_window, height=200)
            note_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
            note_text.insert("1.0", content)
            
            def update_note():
                new_title = title_entry.get().strip()
                new_content = note_text.get("1.0", "end-1c").strip()
                
                if not new_title:
                    new_title = title
                
                if new_content:
                    try:
                        cursor = self.conn.cursor()
                        cursor.execute('''
                            UPDATE notes 
                            SET title = ?, content = ?, modified_date = CURRENT_TIMESTAMP
                            WHERE id = ?
                        ''', (new_title, new_content, note_id))
                        self.conn.commit()
                        
                        messagebox.showinfo("Nota Actualizada", "Nota actualizada exitosamente")
                        self.speak("Nota actualizada correctamente")
                        edit_window.destroy()
                        self.add_to_chat(f"Angie: Nota '{new_title}' actualizada exitosamente")
                    except Exception as e:
                        messagebox.showerror("Error", f"Error al actualizar la nota: {str(e)}")
                        self.add_to_chat("Angie: Error al actualizar la nota")
                else:
                    messagebox.showwarning("Advertencia", "El contenido de la nota no puede estar vacío")
            
            # Botones
            button_frame = ctk.CTkFrame(edit_window)
            button_frame.pack(pady=10)
            
            update_button = ctk.CTkButton(button_frame, text="Actualizar", command=update_note)
            update_button.pack(side="left", padx=5)
            
        except Exception as e:
            self.add_to_chat(f"Angie: Error al editar la nota: {str(e)}")
    
    def delete_note(self, note, parent_window):
        """Eliminar una nota"""
        try:
            note_id, title, content, created_date, modified_date = note
            
            if messagebox.askyesno("Confirmar Eliminación", 
                                 f"¿Estás seguro de que quieres eliminar la nota '{title}'?"):
                cursor = self.conn.cursor()
                cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
                self.conn.commit()
                
                messagebox.showinfo("Nota Eliminada", "Nota eliminada exitosamente")
                self.speak("Nota eliminada correctamente")
                self.add_to_chat(f"Angie: Nota '{title}' eliminada exitosamente")
                
                # Cerrar y reabrir la ventana de notas para actualizar
                parent_window.destroy()
                self.show_all_notes()
                
        except Exception as e:
            self.add_to_chat(f"Angie: Error al eliminar la nota: {str(e)}")
    
    def copy_to_clipboard(self, text):
        """Copiar texto al portapapeles"""
        try:
            import pyperclip
            pyperclip.copy(text)
            self.add_to_chat("Angie: Contenido copiado al portapapeles")
        except Exception as e:
            self.add_to_chat(f"Angie: Error al copiar al portapapeles: {str(e)}")
    
    def search_notes_by_voice_command(self, search_term):
        """Buscar notas por comando de voz"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT id, title, content, created_date, modified_date 
                FROM notes 
                WHERE title LIKE ? OR content LIKE ?
                ORDER BY modified_date DESC
            ''', (f'%{search_term}%', f'%{search_term}%'))
            
            notes = cursor.fetchall()
            
            if notes:
                if len(notes) == 1:
                    note = notes[0]
                    self.speak(f"Encontré una nota: {note[1]}. {note[2]}")
                    self.add_to_chat(f"Angie: Encontré la nota '{note[1]}'")
                else:
                    titles = [note[1] for note in notes]
                    self.speak(f"Encontré {len(notes)} notas: {', '.join(titles)}")
                    self.add_to_chat(f"Angie: Encontré {len(notes)} notas: {', '.join(titles)}")
            else:
                self.speak(f"No encontré notas que contengan '{search_term}'")
                self.add_to_chat(f"Angie: No encontré notas con '{search_term}'")
                
        except Exception as e:
            self.add_to_chat(f"Angie: Error al buscar notas: {str(e)}")
    
    def get_notes_summary(self):
        """Obtener resumen de todas las notas"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM notes')
            count = cursor.fetchone()[0]
            
            if count == 0:
                response = "No tienes notas guardadas"
            elif count == 1:
                response = "Tienes 1 nota guardada"
            else:
                response = f"Tienes {count} notas guardadas"
                
            cursor.execute('SELECT title FROM notes ORDER BY modified_date DESC LIMIT 3')
            recent_notes = cursor.fetchall()
            
            if recent_notes:
                titles = [note[0] for note in recent_notes]
                if count <= 3:
                    response += f". Las notas son: {', '.join(titles)}"
                else:
                    response += f". Las más recientes son: {', '.join(titles)}"
            
            self.speak(response)
            self.add_to_chat(f"Angie: {response}")
            
        except Exception as e:
            self.add_to_chat(f"Angie: Error al obtener resumen de notas: {str(e)}")
    
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
    
    def show_news_window(self, category="general", query="", country="es"):
        """Mostrar ventana de noticias con opciones avanzadas"""
        news_window = ctk.CTkToplevel(self.root)
        news_window.title("📰 Centro de Noticias - Angie")
        news_window.geometry("900x700")
        news_window.resizable(True, True)
        
        # Frame principal
        main_frame = ctk.CTkFrame(news_window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        title_label = ctk.CTkLabel(main_frame, text="📰 Centro de Noticias", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=10)
        
        # Frame de controles
        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(fill="x", padx=10, pady=5)
        
        # Categorías
        category_label = ctk.CTkLabel(controls_frame, text="Categoría:")
        category_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.category_var = ctk.StringVar(value=category)
        category_menu = ctk.CTkOptionMenu(controls_frame, 
                                         values=["general", "business", "entertainment", 
                                                "health", "science", "sports", "technology"],
                                         variable=self.category_var)
        category_menu.grid(row=0, column=1, padx=5, pady=5)
        
        # País
        country_label = ctk.CTkLabel(controls_frame, text="País:")
        country_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        
        self.country_var = ctk.StringVar(value=country)
        country_menu = ctk.CTkOptionMenu(controls_frame,
                                        values=["es", "us", "gb", "fr", "de", "it", "mx", "ar"],
                                        variable=self.country_var)
        country_menu.grid(row=0, column=3, padx=5, pady=5)
        
        # Búsqueda personalizada
        search_label = ctk.CTkLabel(controls_frame, text="Buscar:")
        search_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        self.search_entry = ctk.CTkEntry(controls_frame, placeholder_text="Ej: inteligencia artificial")
        self.search_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        
        # Botón de actualizar
        refresh_button = ctk.CTkButton(controls_frame, text="🔄 Actualizar", 
                                      command=lambda: self.load_news(news_frame))
        refresh_button.grid(row=1, column=3, padx=5, pady=5)
        
        # Configurar columnas
        controls_frame.columnconfigure(1, weight=1)
        controls_frame.columnconfigure(2, weight=1)
        
        # Frame para noticias (scrollable)
        news_frame = ctk.CTkScrollableFrame(main_frame, height=500)
        news_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Cargar noticias iniciales
        self.load_news(news_frame)
        
    def load_news(self, news_frame):
        """Cargar y mostrar noticias"""
        # Limpiar frame
        for widget in news_frame.winfo_children():
            widget.destroy()
            
        # Mostrar indicador de carga
        loading_label = ctk.CTkLabel(news_frame, text="🔄 Cargando noticias...", 
                                    font=ctk.CTkFont(size=16))
        loading_label.pack(pady=20)
        
        # Actualizar interfaz
        news_frame.update()
        
        # Obtener noticias en hilo separado
        threading.Thread(target=self._fetch_and_display_news, 
                        args=(news_frame, loading_label), daemon=True).start()
        
    def _fetch_and_display_news(self, news_frame, loading_label):
        """Obtener y mostrar noticias en hilo separado"""
        try:
            # Verificar API key
            if not NEWS_API_KEY or NEWS_API_KEY == "tu_news_api_key_aqui":
                self.root.after(0, self._display_error, news_frame, loading_label, 
                               "API key de noticias no configurada. Ve a newsapi.org para obtener una gratuita.")
                return
            
            category = self.category_var.get()
            country = self.country_var.get()
            search_query = self.search_entry.get().strip()
            
            # Construir URL de la API
            if search_query:
                url = f"https://newsapi.org/v2/everything?q={search_query}&language={country}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
            else:
                url = f"https://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey={NEWS_API_KEY}"
            
            # Realizar petición
            response = requests.get(url, timeout=15)
            data = response.json()
            
            # Actualizar interfaz en hilo principal
            self.root.after(0, self._display_news_results, news_frame, loading_label, data, response.status_code)
            
        except requests.exceptions.Timeout:
            self.root.after(0, self._display_error, news_frame, loading_label, 
                           "Tiempo de espera agotado. Verifica tu conexión a internet.")
            
        except requests.exceptions.ConnectionError:
            self.root.after(0, self._display_error, news_frame, loading_label, 
                           "Error de conexión. Verifica tu conexión a internet.")
            
        except Exception as e:
            self.root.after(0, self._display_error, news_frame, loading_label, str(e))
            
    def _display_news_results(self, news_frame, loading_label, data, status_code):
        """Mostrar resultados de noticias en la interfaz"""
        loading_label.destroy()
        
        if status_code == 200 and data.get('articles'):
            articles = data['articles'][:10]  # Mostrar máximo 10 noticias
            
            # Título con número de noticias
            header_label = ctk.CTkLabel(news_frame, 
                                       text=f"📰 {len(articles)} noticias encontradas",
                                       font=ctk.CTkFont(size=18, weight="bold"))
            header_label.pack(pady=10)
            
            for i, article in enumerate(articles):
                self._create_news_card(news_frame, article, i)
                
            # Botón para leer resumen de voz
            if articles:
                voice_button = ctk.CTkButton(news_frame, text="🔊 Leer resumen de voz",
                                           command=lambda: self._read_news_summary(articles[:3]))
                voice_button.pack(pady=10)
                
        elif status_code == 401:
            error_label = ctk.CTkLabel(news_frame, text="❌ API key inválida",
                                      font=ctk.CTkFont(size=16))
            error_label.pack(pady=20)
            
            help_label = ctk.CTkLabel(news_frame, 
                                     text="Ve a newsapi.org para obtener una API key gratuita\ny agrégala al archivo .env",
                                     font=ctk.CTkFont(size=12))
            help_label.pack(pady=10)
            
        elif status_code == 429:
            error_label = ctk.CTkLabel(news_frame, text="⏰ Límite de consultas excedido",
                                      font=ctk.CTkFont(size=16))
            error_label.pack(pady=20)
            
            help_label = ctk.CTkLabel(news_frame, 
                                     text="Intenta más tarde o actualiza tu plan en newsapi.org",
                                     font=ctk.CTkFont(size=12))
            help_label.pack(pady=10)
            
        else:
            error_msg = data.get('message', 'No se encontraron noticias') if isinstance(data, dict) else 'Error desconocido'
            error_label = ctk.CTkLabel(news_frame, text=f"❌ {error_msg}",
                                      font=ctk.CTkFont(size=16))
            error_label.pack(pady=20)
            
            # Botón para ayuda de configuración
            if status_code == 401 or not NEWS_API_KEY:
                help_button = ctk.CTkButton(news_frame, text="🔧 Ayuda de configuración",
                                           command=self._show_api_help)
                help_button.pack(pady=10)
            
    def _display_error(self, news_frame, loading_label, error_msg):
        """Mostrar error en la interfaz"""
        loading_label.destroy()
        error_label = ctk.CTkLabel(news_frame, text=f"❌ Error: {error_msg}",
                                  font=ctk.CTkFont(size=16))
        error_label.pack(pady=20)
        
    def _create_news_card(self, parent, article, index):
        """Crear tarjeta individual de noticia"""
        # Frame para la noticia
        card_frame = ctk.CTkFrame(parent)
        card_frame.pack(fill="x", padx=5, pady=5)
        
        # Título de la noticia
        title = article.get('title', 'Sin título')[:100] + ('...' if len(article.get('title', '')) > 100 else '')
        title_label = ctk.CTkLabel(card_frame, text=f"{index + 1}. {title}",
                                  font=ctk.CTkFont(size=14, weight="bold"),
                                  wraplength=800)
        title_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Descripción
        description = article.get('description', 'Sin descripción')
        if description and len(description) > 200:
            description = description[:200] + "..."
        
        desc_label = ctk.CTkLabel(card_frame, text=description,
                                 font=ctk.CTkFont(size=12),
                                 wraplength=800, anchor="w")
        desc_label.pack(anchor="w", padx=10, pady=5)
        
        # Información adicional
        source = article.get('source', {}).get('name', 'Fuente desconocida')
        published_at = article.get('publishedAt', '')
        if published_at:
            try:
                # Formatear fecha
                date_obj = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                published_at = date_obj.strftime('%d/%m/%Y %H:%M')
            except:
                pass
                
        info_text = f"📰 {source} | 📅 {published_at}"
        info_label = ctk.CTkLabel(card_frame, text=info_text,
                                 font=ctk.CTkFont(size=10), 
                                 text_color="gray")
        info_label.pack(anchor="w", padx=10, pady=5)
        
        # Botones de acción
        buttons_frame = ctk.CTkFrame(card_frame)
        buttons_frame.pack(fill="x", padx=10, pady=5)
        
        # Botón leer artículo
        if article.get('url'):
            read_button = ctk.CTkButton(buttons_frame, text="🔗 Leer completa",
                                       command=lambda url=article['url']: webbrowser.open(url),
                                       width=120, height=30)
            read_button.pack(side="left", padx=5)
            
        # Botón escuchar
        listen_button = ctk.CTkButton(buttons_frame, text="🔊 Escuchar",
                                     command=lambda: self._speak_article(article),
                                     width=100, height=30)
        listen_button.pack(side="left", padx=5)
        
        # Botón compartir
        share_button = ctk.CTkButton(buttons_frame, text="📤 Compartir",
                                    command=lambda: self._share_article(article),
                                    width=100, height=30)
        share_button.pack(side="left", padx=5)
        
    def _speak_article(self, article):
        """Leer artículo en voz alta"""
        title = article.get('title', '')
        description = article.get('description', '')
        text_to_speak = f"Noticia: {title}. {description}"
        
        threading.Thread(target=lambda: self.speak(text_to_speak), daemon=True).start()
        
    def _share_article(self, article):
        """Compartir artículo"""
        title = article.get('title', 'Sin título')
        url = article.get('url', '')
        
        share_text = f"{title}\n{url}"
        
        # Copiar al portapapeles
        try:
            import pyperclip
            pyperclip.copy(share_text)
            messagebox.showinfo("Compartir", "Artículo copiado al portapapeles")
        except ImportError:
            # Si pyperclip no está disponible, mostrar ventana con el texto
            share_window = ctk.CTkToplevel(self.root)
            share_window.title("Compartir Artículo")
            share_window.geometry("400x200")
            
            text_widget = ctk.CTkTextbox(share_window)
            text_widget.pack(fill="both", expand=True, padx=10, pady=10)
            text_widget.insert("1.0", share_text)
            
    def _read_news_summary(self, articles):
        """Leer resumen de las principales noticias"""
        summary_text = "Resumen de noticias principales: "
        
        for i, article in enumerate(articles, 1):
            title = article.get('title', 'Sin título')
            summary_text += f"Noticia {i}: {title}. "
            
        threading.Thread(target=lambda: self.speak(summary_text), daemon=True).start()
        
    def get_quick_news_summary(self, category="general"):
        """Obtener resumen rápido de noticias para comandos de voz"""
        try:
            # Verificar si tenemos API key
            if not NEWS_API_KEY or NEWS_API_KEY == "tu_news_api_key_aqui":
                self.speak("Lo siento, necesitas configurar la API key de noticias en el archivo .env")
                self.add_to_chat("Angie: ⚠️ API key de noticias no configurada")
                self.add_to_chat("Angie: Ve a newsapi.org, obtén una API key gratuita y agrégala al archivo .env")
                self.add_to_chat("Angie: Formato: NEWS_API_KEY=tu_api_key_aqui")
                return
            
            # Traducir categoría al español para el mensaje
            category_names = {
                "general": "generales",
                "business": "negocios", 
                "entertainment": "entretenimiento",
                "health": "salud",
                "science": "ciencia", 
                "sports": "deportes",
                "technology": "tecnología"
            }
            category_spanish = category_names.get(category, category)
            
            self.add_to_chat(f"Angie: 🔄 Buscando noticias de {category_spanish}...")
            
            # Lista de países a intentar (ordenados por probabilidad de tener noticias)
            countries_to_try = ["us", "gb", "es"]
            success = False
            
            for country in countries_to_try:
                try:
                    url = f"https://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey={NEWS_API_KEY}"
                    
                    response = requests.get(url, timeout=10)
                    data = response.json()
                    
                    if response.status_code == 200 and data.get('articles') and len(data['articles']) > 0:
                        articles = data['articles'][:3]  # Solo las 3 principales
                        
                        # Información sobre el país usado
                        country_names = {"us": "Estados Unidos", "gb": "Reino Unido", "es": "España"}
                        country_name = country_names.get(country, country.upper())
                        
                        summary = f"Principales noticias de {category_spanish} desde {country_name}: "
                        for i, article in enumerate(articles, 1):
                            title = article.get('title', 'Sin título')
                            # Limpiar el título para lectura de voz
                            title_clean = title.replace('\n', ' ').replace('\r', ' ')
                            summary += f"Noticia {i}: {title_clean}. "
                            
                        self.speak(summary)
                        self.add_to_chat(f"Angie: {summary}")
                        
                        # También mostrar en chat con mejor formato
                        self.add_to_chat(f"Angie: 📰 Top 3 noticias de {category_spanish} ({country_name}):")
                        for i, article in enumerate(articles, 1):
                            title = article.get('title', 'Sin título')
                            source = article.get('source', {}).get('name', 'Fuente desconocida')
                            self.add_to_chat(f"  {i}. {title} ({source})")
                        
                        success = True
                        break
                        
                except requests.exceptions.RequestException:
                    continue
            
            if success:
                return
            
            # Si llegamos aquí, ningún país funcionó, intentar último intento con diagnóstico
            try:
                url = f"https://newsapi.org/v2/top-headlines?country=es&category={category}&apiKey={NEWS_API_KEY}"
                response = requests.get(url, timeout=10)
                data = response.json()
                
                if response.status_code == 401:
                    self.speak("La API key de noticias no es válida")
                    self.add_to_chat("Angie: ❌ API key de noticias inválida")
                    self.add_to_chat("Angie: Verifica tu API key en el archivo .env")
                    
                elif response.status_code == 429:
                    self.speak("Se ha excedido el límite de consultas de noticias")
                    self.add_to_chat("Angie: ⏰ Límite de consultas excedido")
                    self.add_to_chat("Angie: Intenta más tarde o actualiza tu plan en newsapi.org")
                    
                else:
                    error_msg = data.get('message', f'Error HTTP {response.status_code}')
                    self.speak(f"No hay noticias de {category_spanish} disponibles en este momento")
                    self.add_to_chat(f"Angie: ⚠️ No hay noticias de {category_spanish} disponibles")
                    self.add_to_chat("Angie: � Las noticias en español pueden tener disponibilidad limitada")
                    self.add_to_chat("Angie: 🌐 Tip: Usa el centro de noticias para explorar otras fuentes")
            except:
                self.speak(f"No pude obtener noticias de {category_spanish}")
                self.add_to_chat(f"Angie: ❌ Error al obtener noticias de {category_spanish}")
                self.add_to_chat("Angie: 💡 Tip: Haz clic en el botón 'Noticias' para acceder al centro completo")
                
        except requests.exceptions.Timeout:
            self.speak("La conexión tardó demasiado")
            self.add_to_chat("Angie: ⏰ Tiempo de espera agotado. Verifica tu conexión a internet")
            
        except requests.exceptions.ConnectionError:
            self.speak("No hay conexión a internet")
            self.add_to_chat("Angie: 🌐 Error de conexión. Verifica tu conexión a internet")
            
        except Exception as e:
            self.speak("Ocurrió un error al obtener las noticias")
            self.add_to_chat(f"Angie: ❌ Error: {str(e)}")
            self.add_to_chat("Angie: 💡 Tip: Usa el botón 'Noticias' en la interfaz para más opciones")
    
    def _show_api_help(self):
        """Mostrar ayuda para configurar la API de noticias"""
        help_window = ctk.CTkToplevel(self.root)
        help_window.title("🔧 Configuración de API de Noticias")
        help_window.geometry("500x400")
        help_window.resizable(True, True)
        
        # Frame principal
        main_frame = ctk.CTkFrame(help_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(main_frame, text="🔧 Configurar API de Noticias", 
                                  font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=10)
        
        # Instrucciones
        instructions = """
📋 Pasos para configurar las noticias:

1. Ve a https://newsapi.org/
2. Haz clic en "Get API Key" 
3. Crea una cuenta gratuita
4. Copia tu API key

5. Crea un archivo .env en la carpeta del proyecto
6. Agrega esta línea:
   NEWS_API_KEY=tu_api_key_aqui

7. Reinicia la aplicación

✅ ¡Listo! Ya podrás acceder a las noticias.

💡 Plan gratuito: 1,000 consultas/mes
"""
        
        instructions_label = ctk.CTkLabel(main_frame, text=instructions,
                                        font=ctk.CTkFont(size=12),
                                        justify="left")
        instructions_label.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Botones
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="x", pady=10)
        
        # Botón para abrir NewsAPI
        newsapi_button = ctk.CTkButton(buttons_frame, text="🌐 Abrir NewsAPI.org",
                                      command=lambda: webbrowser.open("https://newsapi.org/"))
        newsapi_button.pack(side="left", padx=5)
        
        # Botón cerrar
        close_button = ctk.CTkButton(buttons_frame, text="Cerrar",
                                    command=help_window.destroy)
        close_button.pack(side="right", padx=5)
    
    def show_notes_help(self):
        """Mostrar ayuda sobre los comandos de notas disponibles"""
        help_text = """
📝 COMANDOS DE NOTAS DISPONIBLES:

🗣️ COMANDOS DE VOZ:
• "Crear nota" / "Nueva nota" / "Tomar nota"
• "Ver notas" / "Mostrar notas" / "Mis notas"
• "Buscar nota [término]" - Busca en títulos y contenido
• "Cuántas notas" / "Resumen de notas"
• "Leer notas" - Lee las 3 notas más recientes

💬 COMANDOS DE TEXTO:
Puedes escribir los mismos comandos en el chat de texto.

🖱️ INTERFAZ GRÁFICA:
• Botón "📝 Nueva Nota" - Crear una nueva nota
• Botón "📚 Ver Notas" - Ver todas las notas guardadas
• En cada nota puedes: Leer, Editar, Eliminar, Copiar

✨ CARACTERÍSTICAS:
• Las notas se guardan en base de datos SQLite
• Búsqueda por título y contenido
• Lectura de notas por voz
• Edición y eliminación de notas
• Copia de contenido al portapapeles
• Fechas de creación y modificación
        """
        
        try:
            help_window = ctk.CTkToplevel(self.root)
            help_window.title("Ayuda - Sistema de Notas")
            help_window.geometry("600x500")
            
            help_textbox = ctk.CTkTextbox(help_window)
            help_textbox.pack(fill="both", expand=True, padx=20, pady=20)
            help_textbox.insert("1.0", help_text)
            help_textbox.configure(state="disabled")
            
            self.speak("He abierto la ayuda del sistema de notas")
            self.add_to_chat("Angie: Ayuda del sistema de notas mostrada")
            
        except Exception as e:
            self.add_to_chat(f"Angie: Error al mostrar ayuda: {str(e)}")

# Función principal
def main():
    """Función principal para ejecutar Angie Advanced"""
    try:
        print("🎤 Iniciando Angie Advanced - Asistente Virtual Pro")
        print("=" * 60)
        
        # Verificar archivo .env
        if not os.path.exists('.env'):
            print("⚠️ ADVERTENCIA: No se encuentra el archivo .env")
            print("Copia config_example.txt a .env y configura tus API keys")
            print()
        
        # Crear instancia del asistente
        angie = AngieAdvanced()
        
        print("✅ Angie Advanced iniciado correctamente")
        print("🎯 La interfaz gráfica se está abriendo...")
        print()
        print("💡 Funcionalidades disponibles:")
        print("- 🎤 Comandos de voz (activa con 'Activar Angie')")
        print("- 📰 Centro de noticias avanzado")
        print("- 🌤️ Información del clima")
        print("- 📝 Notas y recordatorios")
        print("- 🔍 Búsquedas en Wikipedia")
        print("- 💻 Información del sistema")
        print("- ✅ Gestión de tareas")
        print()
        
        # Ejecutar la aplicación
        angie.run()
        
    except Exception as e:
        print(f"❌ Error al iniciar Angie Advanced: {str(e)}")
        print()
        print("💡 Posibles soluciones:")
        print("1. Instala las dependencias: pip install -r requirements.txt")
        print("2. Configura tu archivo .env con las API keys")
        print("3. Verifica tu conexión a internet")
        input("Presiona Enter para continuar...")

if __name__ == "__main__":
    main()