# 🧠 Sistema de Entrenamiento LSTM para Angie Assistant

## 📋 Descripción

Este sistema implementa un modelo LSTM (Long Short-Term Memory) para entrenar y mejorar la capacidad de reconocimiento de comandos de tu asistente virtual Angie. El modelo utiliza 2-3 capas LSTM con 64-128 neuronas cada una para clasificar automáticamente los tipos de comandos de voz y texto.

## 🏗️ Arquitectura del Modelo

### Capas LSTM Implementadas:
```
Input (Texto) 
    ↓
Embedding (128 dimensiones)
    ↓
LSTM Capa 1 (128 neuronas, return_sequences=True)
    ↓
LSTM Capa 2 (64 neuronas, return_sequences=True)  
    ↓
LSTM Capa 3 (32 neuronas)
    ↓
Dense (64 neuronas, ReLU)
    ↓
Dropout (0.3)
    ↓
Output (Softmax para clasificación)
```

### Tipos de Comandos Soportados:
- **time**: Consultas de hora y fecha
- **weather**: Información del clima
- **search**: Búsquedas en Wikipedia
- **music**: Reproducción de música
- **notes**: Toma de notas
- **screenshot**: Capturas de pantalla
- **system**: Información del sistema
- **reminder**: Recordatorios
- **news**: Noticias
- **navigation**: Navegación web
- **tasks**: Gestión de tareas
- **chat**: Conversación general

## 🚀 Instalación

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Verificar Instalación
```bash
python run_lstm_training.py --example
```

## 📊 Uso del Sistema

### Entrenamiento Independiente
```bash
python run_lstm_training.py
```

### Entrenamiento con Visualizaciones de Ejemplo
```bash
python run_lstm_training.py --example
```

### Integración con Angie Assistant
```python
from angie_lstm_integration import integrate_with_angie
from angie_advanced import AngieAdvanced

# Crear instancia de Angie
angie = AngieAdvanced()

# Integrar sistema LSTM
integrator = integrate_with_angie(angie)

# Ejecutar asistente
angie.run()
```

## 📈 Visualizaciones Generadas

El sistema genera automáticamente las siguientes visualizaciones:

### 1. Curvas de Entrenamiento
- **Archivo**: `training_plots/training_curves.png`
- **Contenido**: Evolución de pérdida y precisión durante el entrenamiento
- **Análisis**: Permite identificar overfitting y convergencia

### 2. Matriz de Confusión
- **Archivo**: `training_plots/confusion_matrix.png`
- **Contenido**: Matriz de confusión del modelo entrenado
- **Análisis**: Muestra qué tipos de comandos se confunden entre sí

### 3. Distribución de Comandos
- **Archivo**: `training_plots/command_distribution.png`
- **Contenido**: Frecuencia de cada tipo de comando
- **Análisis**: Identifica comandos poco representados

### 4. Análisis de Longitud
- **Archivo**: `training_plots/command_length_analysis.png`
- **Contenido**: Distribución de longitud de comandos
- **Análisis**: Optimización del padding y tokenización

### 5. Frecuencia de Palabras
- **Archivo**: `training_plots/word_frequency.png`
- **Contenido**: Palabras más frecuentes en comandos
- **Análisis**: Vocabulario más utilizado

### 6. Resumen de Métricas
- **Archivo**: `training_plots/metrics_summary.png`
- **Contenido**: Dashboard completo de métricas
- **Análisis**: Vista general del rendimiento

## 🔧 Configuración Avanzada

### Parámetros del Modelo
```python
# En angie_lstm_trainer.py
class AngieLSTMTrainer:
    def __init__(self, db_path='angie_data.db', max_words=1000, max_len=50):
        # max_words: Tamaño del vocabulario
        # max_len: Longitud máxima de secuencia
```

### Hiperparámetros de Entrenamiento
```python
# En el método train_model()
epochs=50          # Número de épocas
batch_size=32      # Tamaño del batch
dropout=0.2        # Dropout en capas LSTM
dropout_dense=0.3  # Dropout en capa densa
```

### Callbacks Configurados
- **EarlyStopping**: Detiene el entrenamiento si no mejora
- **ReduceLROnPlateau**: Reduce el learning rate automáticamente

## 📊 Base de Datos

### Tabla de Interacciones
```sql
CREATE TABLE interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_input TEXT NOT NULL,
    assistant_response TEXT NOT NULL,
    command_type TEXT,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    confidence REAL DEFAULT 0.0
);
```

### Estructura de Datos
- **user_input**: Comando original del usuario
- **assistant_response**: Respuesta del asistente
- **command_type**: Tipo de comando detectado
- **timestamp**: Fecha y hora de la interacción
- **confidence**: Confianza de la clasificación

## 🔮 Predicciones en Tiempo Real

### Uso del Modelo Entrenado
```python
from angie_lstm_trainer import AngieLSTMTrainer

trainer = AngieLSTMTrainer()
trainer.load_model()  # Cargar modelo existente

# Predecir tipo de comando
prediction = trainer.predict_command_type("¿qué hora es?")
print(f"Tipo: {prediction['command_type']}")
print(f"Confianza: {prediction['confidence']:.2f}")
```

## 📈 Métricas de Rendimiento

### Métricas Calculadas
- **Precisión**: Porcentaje de predicciones correctas
- **Matriz de Confusión**: Detalle de aciertos y errores
- **Distribución de Clases**: Balance de tipos de comandos
- **Vocabulario Único**: Variedad de palabras utilizadas

### Recomendaciones Automáticas
El sistema genera recomendaciones basadas en:
- Distribución desbalanceada de comandos
- Vocabulario limitado
- Patrones de uso detectados

## 🔄 Entrenamiento Automático

### Configuración de Entrenamiento Automático
```python
# Iniciar entrenamiento automático cada 24 horas
integrator.start_auto_training(interval_hours=24)
```

### Logs de Entrenamiento
- Registro automático de todas las interacciones
- Análisis de tendencias de uso
- Recomendaciones de mejora

## 🛠️ Solución de Problemas

### Error: "No module named 'tensorflow'"
```bash
pip install tensorflow
```

### Error: "CUDA not available"
- El modelo funciona con CPU, pero es más lento
- Para GPU: `pip install tensorflow-gpu`

### Error: "Not enough data"
- El sistema genera datos de ejemplo automáticamente
- Usa más comandos para mejorar el entrenamiento

### Baja Precisión
1. Aumentar datos de entrenamiento
2. Ajustar hiperparámetros
3. Revisar distribución de clases
4. Verificar calidad de datos

## 📁 Estructura de Archivos

```
AsistenteVirtual/
├── angie_advanced.py          # Asistente principal
├── angie_lstm_trainer.py      # Entrenador LSTM
├── angie_lstm_integration.py  # Integración con asistente
├── run_lstm_training.py       # Script principal
├── requirements.txt           # Dependencias
├── README_LSTM.md            # Esta documentación
├── training_plots/           # Visualizaciones generadas
│   ├── training_curves.png
│   ├── confusion_matrix.png
│   ├── command_distribution.png
│   ├── command_length_analysis.png
│   ├── word_frequency.png
│   └── metrics_summary.png
└── angie_data.db             # Base de datos SQLite
```

## 🎯 Próximos Pasos

1. **Recopilar más datos**: Usa el asistente más frecuentemente
2. **Diversificar comandos**: Prueba diferentes formas de expresar comandos
3. **Re-entrenar periódicamente**: Ejecuta el entrenamiento cada semana
4. **Analizar visualizaciones**: Usa las gráficas para optimizar
5. **Expandir tipos de comando**: Agrega nuevos tipos según necesidades

## 🤝 Contribuciones

Para mejorar el sistema:
1. Reporta bugs en el entrenamiento
2. Sugiere nuevos tipos de comandos
3. Optimiza hiperparámetros
4. Mejora visualizaciones

## 📞 Soporte

Si tienes problemas:
1. Verifica que todas las dependencias estén instaladas
2. Revisa los logs de error
3. Ejecuta con datos de ejemplo primero
4. Consulta la documentación de TensorFlow

---

**¡Disfruta entrenando tu asistente virtual con LSTM! 🚀** 