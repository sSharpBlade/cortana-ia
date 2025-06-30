#!/usr/bin/env python3
"""
Angie Assistant con Sistema LSTM Integrado
Combina la funcionalidad original con entrenamiento LSTM automático
"""

import sys
import os
import threading
import time
from datetime import datetime

# Importar el asistente original
try:
    from angie_advanced import AngieAdvanced
    print("✅ Módulo angie_advanced importado correctamente")
except ImportError as e:
    print(f"❌ Error importando angie_advanced: {e}")
    print("💡 Asegúrate de que angie_advanced.py esté en el mismo directorio")
    sys.exit(1)

# Importar sistema LSTM
try:
    from angie_lstm_integration import integrate_with_angie, AngieLSTMIntegration
    print("✅ Sistema LSTM importado correctamente")
except ImportError as e:
    print(f"⚠️  Sistema LSTM no disponible: {e}")
    print("💡 Para usar LSTM, instala las dependencias: python install_lstm_dependencies.py")

class AngieWithLSTM:
    def __init__(self):
        """Inicializar Angie con sistema LSTM integrado"""
        print("🚀 Iniciando Angie Assistant con LSTM...")
        
        # Crear instancia del asistente original
        self.angie = AngieAdvanced()
        
        # Intentar integrar sistema LSTM
        self.lstm_available = False
        try:
            self.integrator = integrate_with_angie(self.angie)
            self.lstm_available = True
            print("✅ Sistema LSTM integrado exitosamente")
            
            # Agregar botón de entrenamiento manual
            self.add_lstm_controls()
            
        except Exception as e:
            print(f"⚠️  Sistema LSTM no disponible: {e}")
            print("💡 El asistente funcionará sin LSTM")
    
    def add_lstm_controls(self):
        """Agregar controles LSTM a la interfaz"""
        try:
            # Agregar información LSTM al área de chat
            self.angie.add_to_chat("🧠 Sistema LSTM integrado y listo")
            self.angie.add_to_chat("📊 Las interacciones se registran automáticamente")
            self.angie.add_to_chat("🎯 Usa el botón '🧠 Entrenar LSTM' para entrenar el modelo")
            
            # Agregar comando de voz para entrenamiento
            original_process_command = self.angie.process_command
            
            def enhanced_process_command(command):
                # Procesar comando original
                original_process_command(command)
                
                # Verificar si es comando de entrenamiento LSTM
                if any(word in command.lower() for word in ['entrena', 'lstm', 'modelo', 'aprende']):
                    self.start_lstm_training()
            
            self.angie.process_command = enhanced_process_command
            
        except Exception as e:
            print(f"⚠️  Error agregando controles LSTM: {e}")
    
    def start_lstm_training(self):
        """Iniciar entrenamiento LSTM en hilo separado"""
        if not self.lstm_available:
            self.angie.add_to_chat("❌ Sistema LSTM no disponible")
            return
        
        def train_thread():
            try:
                self.angie.add_to_chat("🧠 Iniciando entrenamiento LSTM...")
                self.angie.speak("Iniciando entrenamiento del modelo LSTM")
                
                # Ejecutar entrenamiento
                results = self.integrator.trainer.run_full_training()
                
                # Mostrar resultados
                accuracy = results['accuracy']
                self.angie.add_to_chat(f"✅ Entrenamiento LSTM completado")
                self.angie.add_to_chat(f"📊 Precisión: {accuracy:.2%}")
                self.angie.speak(f"Entrenamiento completado con precisión del {accuracy:.1%}")
                
                # Mostrar recomendaciones
                recommendations = self.integrator.get_training_recommendations()
                self.angie.add_to_chat("💡 Recomendaciones:")
                for rec in recommendations:
                    self.angie.add_to_chat(f"   • {rec}")
                
                # Mostrar estadísticas
                stats = self.integrator.get_interaction_stats()
                self.angie.add_to_chat(f"📈 Total interacciones: {stats['total_interactions']}")
                
            except Exception as e:
                self.angie.add_to_chat(f"❌ Error en entrenamiento LSTM: {e}")
                self.angie.speak("Error en el entrenamiento del modelo")
        
        # Ejecutar en hilo separado
        threading.Thread(target=train_thread, daemon=True).start()
    
    def show_lstm_stats(self):
        """Mostrar estadísticas del sistema LSTM"""
        if not self.lstm_available:
            self.angie.add_to_chat("❌ Sistema LSTM no disponible")
            return
        
        try:
            stats = self.integrator.get_interaction_stats()
            
            self.angie.add_to_chat("📊 Estadísticas LSTM:")
            self.angie.add_to_chat(f"   • Total interacciones: {stats['total_interactions']}")
            
            if stats['command_types']:
                self.angie.add_to_chat("   • Distribución de comandos:")
                for cmd_type, count in stats['command_types'].items():
                    percentage = (count / stats['total_interactions']) * 100
                    self.angie.add_to_chat(f"     - {cmd_type}: {count} ({percentage:.1f}%)")
            
            # Mostrar actividad reciente
            if stats['recent_activity']:
                self.angie.add_to_chat("   • Actividad reciente:")
                for activity in stats['recent_activity'][-3:]:  # Últimas 3
                    self.angie.add_to_chat(f"     - {activity['command_type']}: {activity['user_input'][:30]}...")
            
        except Exception as e:
            self.angie.add_to_chat(f"❌ Error obteniendo estadísticas: {e}")
    
    def predict_command(self, text):
        """Predecir tipo de comando usando LSTM"""
        if not self.lstm_available:
            return None
        
        try:
            prediction = self.integrator.predict_next_command(text)
            if prediction and prediction['confidence'] > 0.7:
                return prediction
        except Exception as e:
            print(f"Error en predicción: {e}")
        
        return None
    
    def run(self):
        """Ejecutar el asistente con LSTM"""
        print("🎤 Iniciando Angie Assistant con LSTM...")
        
        # Mostrar información de inicio
        if self.lstm_available:
            print("🧠 Sistema LSTM: ACTIVO")
            print("📊 Interacciones se registran automáticamente")
            print("🎯 Comandos de entrenamiento disponibles:")
            print("   - 'entrena lstm' o 'entrena modelo'")
            print("   - 'estadísticas lstm' o 'stats lstm'")
        else:
            print("⚠️  Sistema LSTM: NO DISPONIBLE")
            print("💡 Para activar LSTM: python install_lstm_dependencies.py")
        
        print("\n🎤 Comandos de voz disponibles:")
        print("   - 'Angie, ¿qué hora es?'")
        print("   - 'Angie, dime el clima'")
        print("   - 'Angie, reproduce música'")
        print("   - 'Angie, busca información sobre...'")
        print("   - 'Angie, toma una nota'")
        print("   - 'Angie, captura de pantalla'")
        print("   - 'Angie, información del sistema'")
        print("   - 'Angie, agrega recordatorio'")
        print("   - 'Angie, busca noticias'")
        print("   - 'Angie, abre [sitio web]'")
        print("   - 'Angie, muestra mis tareas'")
        
        if self.lstm_available:
            print("\n🧠 Comandos LSTM adicionales:")
            print("   - 'Angie, entrena lstm'")
            print("   - 'Angie, estadísticas lstm'")
            print("   - 'Angie, predice comando [texto]'")
        
        print("\n" + "="*60)
        print("🚀 ¡Angie Assistant con LSTM está listo!")
        print("="*60)
        
        # Ejecutar asistente
        try:
            self.angie.run()
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
        except Exception as e:
            print(f"❌ Error ejecutando asistente: {e}")

def main():
    """Función principal"""
    print("🧠 ANGIELSTM - Asistente Virtual con Aprendizaje Automático")
    print("=" * 60)
    
    # Verificar archivos necesarios
    required_files = ['angie_advanced.py']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Faltan archivos necesarios:")
        for file in missing_files:
            print(f"   - {file}")
        print("\n💡 Asegúrate de que todos los archivos estén en el mismo directorio")
        return
    
    # Crear y ejecutar asistente con LSTM
    try:
        angie_lstm = AngieWithLSTM()
        angie_lstm.run()
    except Exception as e:
        print(f"❌ Error iniciando Angie con LSTM: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 