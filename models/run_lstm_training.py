#!/usr/bin/env python3
"""
Script principal para entrenamiento LSTM de Angie Assistant
Genera visualizaciones completas del entrenamiento del modelo
"""

import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Configurar matplotlib para mejor visualización
plt.style.use('default')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3

def print_banner():
    """Imprimir banner del entrenamiento"""
    print("=" * 80)
    print("🧠 ANGIELSTM TRAINER - Sistema de Entrenamiento LSTM para Angie Assistant")
    print("=" * 80)
    print("📊 Generando visualizaciones de entrenamiento con 2-3 capas LSTM")
    print("🎯 Neuronas: 128 -> 64 -> 32 por capa")
    print("=" * 80)

def check_dependencies():
    """Verificar dependencias necesarias"""
    required_packages = [
        'tensorflow', 'numpy', 'pandas', 'matplotlib', 
        'seaborn', 'sklearn', 'sqlite3'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Faltan dependencias:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Instala las dependencias con:")
        print("pip install tensorflow numpy pandas matplotlib seaborn scikit-learn")
        return False
    
    print("✅ Todas las dependencias están instaladas")
    return True

def main():
    """Función principal"""
    print_banner()
    
    # Verificar dependencias
    if not check_dependencies():
        return
    
    try:
        # Importar módulos después de verificar dependencias
        from angie_lstm_trainer import AngieLSTMTrainer
        from angie_lstm_integration import AngieLSTMIntegration
        
        print("\n🚀 Iniciando proceso de entrenamiento LSTM...")
        
        # Crear instancia del entrenador
        trainer = AngieLSTMTrainer()
        
        # Ejecutar entrenamiento completo
        print("\n📊 Paso 1: Cargando y preprocesando datos...")
        results = trainer.run_full_training()
        
        # Mostrar resultados
        print("\n" + "=" * 50)
        print("📈 RESULTADOS DEL ENTRENAMIENTO")
        print("=" * 50)
        print(f"🎯 Precisión final: {results['accuracy']:.2%}")
        print(f"📊 Clases de comandos: {len(results['class_names'])}")
        print(f"📁 Visualizaciones guardadas en: training_plots/")
        
        # Mostrar información del modelo
        print("\n🧠 ARQUITECTURA DEL MODELO LSTM:")
        print("   • Capa de Embedding: 128 dimensiones")
        print("   • LSTM Capa 1: 128 neuronas (return_sequences=True)")
        print("   • LSTM Capa 2: 64 neuronas (return_sequences=True)")
        print("   • LSTM Capa 3: 32 neuronas")
        print("   • Dense: 64 neuronas (ReLU)")
        print("   • Dropout: 0.3")
        print("   • Salida: Softmax para clasificación")
        
        # Crear integrador para análisis adicional
        print("\n📊 Paso 2: Analizando datos de interacciones...")
        integrator = AngieLSTMIntegration()
        
        # Obtener estadísticas
        stats = integrator.get_interaction_stats()
        print(f"📈 Total de interacciones: {stats['total_interactions']}")
        
        if stats['command_types']:
            print("📊 Distribución de comandos:")
            for cmd_type, count in stats['command_types'].items():
                percentage = (count / stats['total_interactions']) * 100
                print(f"   • {cmd_type}: {count} ({percentage:.1f}%)")
        
        # Obtener recomendaciones
        print("\n💡 RECOMENDACIONES DE ENTRENAMIENTO:")
        recommendations = integrator.get_training_recommendations()
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
        
        # Crear resumen final
        print("\n" + "=" * 50)
        print("🎉 ENTRENAMIENTO COMPLETADO EXITOSAMENTE")
        print("=" * 50)
        print("📁 Archivos generados:")
        
        # Listar archivos generados
        if os.path.exists('training_plots'):
            for file in os.listdir('training_plots'):
                if file.endswith('.png'):
                    print(f"   • training_plots/{file}")
        
        model_files = ['angie_lstm_model.h5', 'angie_lstm_model_tokenizer.pkl', 'angie_lstm_model_label_encoder.pkl']
        for file in model_files:
            if os.path.exists(file):
                print(f"   • {file}")
        
        print("\n🔮 PRÓXIMOS PASOS:")
        print("   1. Usa el modelo entrenado en tu asistente")
        print("   2. Ejecuta más interacciones para mejorar el modelo")
        print("   3. Re-entrena periódicamente con nuevos datos")
        print("   4. Analiza las visualizaciones para optimizar")
        
        # Probar predicción
        print("\n🧪 PRUEBA DE PREDICCIÓN:")
        test_commands = [
            "¿qué hora es?",
            "dime el clima",
            "reproduce música",
            "busca información"
        ]
        
        for cmd in test_commands:
            prediction = trainer.predict_command_type(cmd)
            if prediction != "Modelo no entrenado":
                print(f"   • '{cmd}' -> {prediction['command_type']} (confianza: {prediction['confidence']:.2f})")
        
        print("\n✅ ¡Proceso completado! Revisa las visualizaciones en la carpeta 'training_plots'")
        
    except ImportError as e:
        print(f"❌ Error importando módulos: {e}")
        print("💡 Asegúrate de que todos los archivos estén en el mismo directorio")
    except Exception as e:
        print(f"❌ Error durante el entrenamiento: {e}")
        import traceback
        traceback.print_exc()

def create_sample_visualizations():
    """Crear visualizaciones de ejemplo si no hay datos reales"""
    print("\n📊 Creando visualizaciones de ejemplo...")
    
    # Crear directorio
    os.makedirs('training_plots', exist_ok=True)
    
    # 1. Curvas de entrenamiento simuladas
    epochs = np.arange(1, 21)
    train_loss = 2.5 * np.exp(-epochs/5) + 0.1 + np.random.normal(0, 0.05, 20)
    val_loss = 2.3 * np.exp(-epochs/4.5) + 0.15 + np.random.normal(0, 0.08, 20)
    train_acc = 1 - 0.8 * np.exp(-epochs/4) + np.random.normal(0, 0.02, 20)
    val_acc = 1 - 0.85 * np.exp(-epochs/3.5) + np.random.normal(0, 0.03, 20)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    ax1.plot(epochs, train_loss, 'b-', label='Pérdida de Entrenamiento', linewidth=2)
    ax1.plot(epochs, val_loss, 'r-', label='Pérdida de Validación', linewidth=2)
    ax1.set_title('Evolución de la Pérdida', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Época')
    ax1.set_ylabel('Pérdida')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(epochs, train_acc, 'b-', label='Precisión de Entrenamiento', linewidth=2)
    ax2.plot(epochs, val_acc, 'r-', label='Precisión de Validación', linewidth=2)
    ax2.set_title('Evolución de la Precisión', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Época')
    ax2.set_ylabel('Precisión')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('training_plots/training_curves_example.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Matriz de confusión simulada
    command_types = ['time', 'weather', 'search', 'music', 'notes', 'screenshot', 'system', 'chat']
    confusion_matrix = np.array([
        [15, 1, 0, 0, 0, 0, 0, 1],
        [1, 12, 1, 0, 0, 0, 0, 0],
        [0, 1, 18, 1, 0, 0, 0, 0],
        [0, 0, 1, 14, 1, 0, 0, 0],
        [0, 0, 0, 1, 10, 0, 0, 0],
        [0, 0, 0, 0, 0, 8, 0, 0],
        [0, 0, 0, 0, 0, 0, 6, 0],
        [1, 0, 0, 0, 0, 0, 0, 20]
    ])
    
    plt.figure(figsize=(10, 8))
    import seaborn as sns
    sns.heatmap(confusion_matrix, annot=True, fmt='d', cmap='Blues', 
               xticklabels=command_types, yticklabels=command_types)
    plt.title('Matriz de Confusión - Ejemplo', fontsize=16, fontweight='bold')
    plt.xlabel('Predicción', fontsize=12)
    plt.ylabel('Valor Real', fontsize=12)
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig('training_plots/confusion_matrix_example.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Visualizaciones de ejemplo creadas en 'training_plots/'")

if __name__ == "__main__":
    # Verificar si se quiere crear visualizaciones de ejemplo
    if len(sys.argv) > 1 and sys.argv[1] == "--example":
        create_sample_visualizations()
    else:
        main() 