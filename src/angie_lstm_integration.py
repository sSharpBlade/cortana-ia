import sqlite3
import pandas as pd
from datetime import datetime
import threading
import time
from angie_lstm_trainer import AngieLSTMTrainer

class AngieLSTMIntegration:
    def __init__(self, db_path='angie_data.db'):
        self.db_path = db_path
        self.trainer = AngieLSTMTrainer(db_path)
        self.setup_interaction_table()
        
    def setup_interaction_table(self):
        """Configurar tabla de interacciones en la base de datos existente"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute('''
                CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_input TEXT NOT NULL,
                    assistant_response TEXT NOT NULL,
                    command_type TEXT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    confidence REAL DEFAULT 0.0
                )
            ''')
            conn.commit()
            conn.close()
            print("✅ Tabla de interacciones configurada")
        except Exception as e:
            print(f"❌ Error configurando tabla: {e}")
    
    def log_interaction(self, user_input, assistant_response, command_type="unknown", confidence=0.0):
        """Registrar una interacción en la base de datos"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute('''
                INSERT INTO interactions (user_input, assistant_response, command_type, confidence)
                VALUES (?, ?, ?, ?)
            ''', (user_input, assistant_response, command_type, confidence))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Error registrando interacción: {e}")
            return False
    
    def detect_command_type(self, user_input):
        """Detectar automáticamente el tipo de comando basado en palabras clave"""
        user_input_lower = user_input.lower()
        
        # Mapeo de palabras clave a tipos de comando
        command_patterns = {
            'time': ['hora', 'tiempo', 'qué hora', 'qué día'],
            'weather': ['clima', 'tiempo', 'temperatura', 'lluvia'],
            'search': ['busca', 'buscar', 'encuentra', 'información'],
            'music': ['reproduce', 'música', 'spotify', 'youtube'],
            'notes': ['nota', 'anota', 'escribe', 'apunta'],
            'screenshot': ['captura', 'screenshot', 'pantalla'],
            'system': ['sistema', 'computadora', 'cpu', 'ram', 'disco'],
            'reminder': ['recordatorio', 'recordar', 'recordar'],
            'news': ['noticias', 'noticia', 'actualidad'],
            'navigation': ['abre', 'navega', 'ir a', 'visita'],
            'tasks': ['tarea', 'tareas', 'pendiente'],
            'chat': ['hola', 'cómo estás', 'chiste', 'conversa']
        }
        
        for command_type, patterns in command_patterns.items():
            for pattern in patterns:
                if pattern in user_input_lower:
                    return command_type
        
        return 'chat'  # Por defecto
    
    def get_interaction_stats(self):
        """Obtener estadísticas de las interacciones"""
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query("SELECT * FROM interactions", conn)
            conn.close()
            
            if df.empty:
                return {
                    'total_interactions': 0,
                    'command_types': {},
                    'recent_activity': []
                }
            
            stats = {
                'total_interactions': len(df),
                'command_types': df['command_type'].value_counts().to_dict(),
                'recent_activity': df.tail(10)[['user_input', 'command_type', 'timestamp']].to_dict('records')
            }
            
            return stats
        except Exception as e:
            print(f"❌ Error obteniendo estadísticas: {e}")
            return {}
    
    def start_auto_training(self, interval_hours=24):
        """Iniciar entrenamiento automático en intervalos"""
        def auto_train():
            while True:
                try:
                    print("🔄 Iniciando entrenamiento automático...")
                    results = self.trainer.run_full_training()
                    print(f"✅ Entrenamiento automático completado. Precisión: {results['accuracy']:.2%}")
                except Exception as e:
                    print(f"❌ Error en entrenamiento automático: {e}")
                
                # Esperar hasta el siguiente entrenamiento
                time.sleep(interval_hours * 3600)
        
        # Iniciar en hilo separado
        training_thread = threading.Thread(target=auto_train, daemon=True)
        training_thread.start()
        print(f"🔄 Entrenamiento automático iniciado (cada {interval_hours} horas)")
    
    def predict_next_command(self, user_input):
        """Predecir el tipo de comando usando el modelo LSTM entrenado"""
        try:
            if self.trainer.model is None:
                # Intentar cargar modelo existente
                if not self.trainer.load_model():
                    return None
            
            prediction = self.trainer.predict_command_type(user_input)
            return prediction
        except Exception as e:
            print(f"❌ Error en predicción: {e}")
            return None
    
    def get_training_recommendations(self):
        """Obtener recomendaciones basadas en los datos de entrenamiento"""
        try:
            stats = self.get_interaction_stats()
            
            if stats['total_interactions'] == 0:
                return "No hay suficientes datos para recomendaciones"
            
            recommendations = []
            
            # Analizar distribución de comandos
            command_types = stats['command_types']
            total = stats['total_interactions']
            
            for cmd_type, count in command_types.items():
                percentage = (count / total) * 100
                if percentage < 5:
                    recommendations.append(f"Considera agregar más ejemplos de comandos '{cmd_type}' (solo {percentage:.1f}%)")
                elif percentage > 40:
                    recommendations.append(f"El comando '{cmd_type}' es muy frecuente ({percentage:.1f}%), considera diversificar")
            
            # Verificar variedad de vocabulario
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query("SELECT user_input FROM interactions", conn)
            conn.close()
            
            all_words = ' '.join(df['user_input'].str.lower()).split()
            unique_words = len(set(all_words))
            
            if unique_words < 50:
                recommendations.append(f"Pocas palabras únicas ({unique_words}), considera usar más variedad en los comandos")
            
            return recommendations if recommendations else ["Los datos de entrenamiento se ven bien"]
            
        except Exception as e:
            return [f"Error analizando recomendaciones: {e}"]

# Función para integrar con el asistente existente
def integrate_with_angie(angie_instance):
    """Integrar el sistema LSTM con una instancia de AngieAdvanced"""
    
    # Crear integrador
    integrator = AngieLSTMIntegration()
    
    # Guardar referencia al método original de process_command
    original_process_command = angie_instance.process_command
    
    def enhanced_process_command(command):
        """Versión mejorada de process_command con logging LSTM"""
        
        # Detectar tipo de comando
        command_type = integrator.detect_command_type(command)
        
        # Procesar comando original
        original_process_command(command)
        
        # Obtener la última respuesta del chat
        chat_content = angie_instance.chat_area.get("end-2l", "end-1c")
        if chat_content.startswith("Angie: "):
            assistant_response = chat_content[7:]  # Remover "Angie: "
        else:
            assistant_response = "Comando procesado"
        
        # Registrar interacción
        integrator.log_interaction(command, assistant_response, command_type)
        
        # Mostrar predicción LSTM si está disponible
        prediction = integrator.predict_next_command(command)
        if prediction and prediction['confidence'] > 0.7:
            angie_instance.add_to_chat(f"🤖 LSTM predijo: {prediction['command_type']} (confianza: {prediction['confidence']:.2f})")
    
    # Reemplazar método
    angie_instance.process_command = enhanced_process_command
    
    # Agregar botón de entrenamiento LSTM a la interfaz
    def add_lstm_training_button():
        """Agregar botón de entrenamiento LSTM a la interfaz"""
        try:
            # Buscar el frame de comandos rápidos
            for widget in angie_instance.root.winfo_children():
                if hasattr(widget, 'winfo_children'):
                    for child in widget.winfo_children():
                        if hasattr(child, 'winfo_children'):
                            for grandchild in child.winfo_children():
                                if isinstance(grandchild, ctk.CTkFrame):
                                    # Agregar botón de entrenamiento
                                    train_button = ctk.CTkButton(
                                        grandchild, 
                                        text="🧠 Entrenar LSTM", 
                                        command=lambda: start_lstm_training(),
                                        width=120
                                    )
                                    train_button.grid(row=2, column=4, padx=5, pady=5)
                                    return
        except Exception as e:
            print(f"Error agregando botón LSTM: {e}")
    
    def start_lstm_training():
        """Iniciar entrenamiento LSTM en hilo separado"""
        def train_thread():
            try:
                angie_instance.add_to_chat("🧠 Iniciando entrenamiento LSTM...")
                results = integrator.trainer.run_full_training()
                angie_instance.add_to_chat(f"✅ Entrenamiento LSTM completado. Precisión: {results['accuracy']:.2%}")
                
                # Mostrar recomendaciones
                recommendations = integrator.get_training_recommendations()
                angie_instance.add_to_chat("📊 Recomendaciones de entrenamiento:")
                for rec in recommendations:
                    angie_instance.add_to_chat(f"   • {rec}")
                    
            except Exception as e:
                angie_instance.add_to_chat(f"❌ Error en entrenamiento LSTM: {e}")
        
        threading.Thread(target=train_thread, daemon=True).start()
    
    # Agregar botón después de que la interfaz esté creada
    angie_instance.root.after(1000, add_lstm_training_button)
    
    return integrator

# Función para ejecutar entrenamiento independiente
def run_standalone_training():
    """Ejecutar entrenamiento LSTM de forma independiente"""
    print("🚀 Iniciando entrenamiento LSTM independiente...")
    
    integrator = AngieLSTMIntegration()
    
    # Mostrar estadísticas actuales
    stats = integrator.get_interaction_stats()
    print(f"📊 Interacciones totales: {stats['total_interactions']}")
    print(f"📊 Tipos de comandos: {stats['command_types']}")
    
    # Ejecutar entrenamiento
    results = integrator.trainer.run_full_training()
    
    # Mostrar recomendaciones
    recommendations = integrator.get_training_recommendations()
    print("\n📊 Recomendaciones:")
    for rec in recommendations:
        print(f"   • {rec}")
    
    return results

if __name__ == "__main__":
    # Ejecutar entrenamiento independiente
    run_standalone_training() 