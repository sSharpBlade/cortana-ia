# 🎤 Angie Advanced - Asistente Virtual Pro

Un asistente virtual inteligente con capacidades avanzadas de procesamiento de lenguaje natural, reconocimiento de voz y integración con APIs externas.

## 📁 Estructura del Proyecto

```
Cortana/
├── 📂 src/                     # Código fuente principal
│   ├── angie_advanced.py       # Asistente principal con GUI
│   ├── angie_advanced_temp.py  # Versión temporal
│   ├── angie_assistant.py      # Versión básica del asistente
│   ├── angie_lstm_integration.py # Integración con LSTM
│   ├── angie_with_lstm.py      # Asistente con modelo LSTM
│   ├── asistente_rnn.py        # Versión con RNN
│   ├── spoty.py                # Integración con Spotify
│   └── version1.py             # Primera versión
│
├── 📂 models/                  # Modelos de ML y entrenamiento
│   ├── angie_lstm_trainer.py   # Entrenador LSTM
│   ├── entrenar_rnn.py         # Entrenador RNN
│   ├── run_lstm_training.py    # Script de entrenamiento
│   ├── modelo_rnn_comandos.h5  # Modelo RNN entrenado
│   └── tokenizer.pickle        # Tokenizador
│
├── 📂 tests/                   # Archivos de pruebas
│   ├── test_news_api.py        # Pruebas de API de noticias
│   ├── test_notes_system.py    # Pruebas del sistema de notas
│   ├── test_search_system.py   # Pruebas de búsqueda
│   ├── test_voice.py           # Pruebas de reconocimiento de voz
│   └── test_weather_api.py     # Pruebas de API del clima
│
├── 📂 demos/                   # Archivos de demostración
│   ├── demo_clima.py           # Demo del sistema de clima
│   ├── demo_notes_interactive.py # Demo interactivo de notas
│   └── demo_noticias.py        # Demo del sistema de noticias
│
├── 📂 docs/                    # Documentación
│   ├── README.md               # Documentación principal
│   ├── README_LSTM.md          # Documentación LSTM
│   ├── README_NOTAS.md         # Documentación de notas
│   ├── README_NOTICIAS.md      # Documentación de noticias
│   ├── README_WEATHERAPI.md    # Documentación del clima
│   ├── INSTRUCCIONES_LSTM.md   # Instrucciones LSTM
│   ├── MEJORAS_NOTAS_COMPLETADAS.md # Log de mejoras
│   └── SOLUCION_BUSQUEDAS.md   # Soluciones de búsqueda
│
├── 📂 data/                    # Archivos de datos
│   ├── angie_data.db           # Base de datos principal
│   ├── historial_comandos.csv  # Historial de comandos
│   └── nota_*.txt              # Archivos de notas
│
├── 📂 media/                   # Imágenes y multimedia
│   └── screenshot_*.png        # Capturas de pantalla
│
├── 📂 utils/                   # Utilidades y scripts auxiliares
│   ├── check_config.py         # Verificador de configuración
│   ├── init_database.py        # Inicializador de BD
│   ├── install_lstm_dependencies.py # Instalador LSTM
│   ├── install_visualization_deps.py # Instalador visualización
│   ├── generate_sample_plots.py # Generador de gráficos
│   ├── open_dashboard.py       # Abridor de dashboard
│   └── visualize_training.py   # Visualizador de entrenamiento
│
├── 📂 config/                  # Archivos de configuración
│   └── config_example.txt      # Ejemplo de configuración
│
├── 📂 training_plots/          # Gráficos de entrenamiento
│   ├── command_distribution.svg
│   ├── training_loss.svg
│   ├── dashboard.html
│   ├── model_example.txt
│   └── training_report.txt
│
├── 📂 front/                   # Frontend (futuro)
├── 📂 legacy/                  # Código legacy
└── requirements.txt            # Dependencias del proyecto
```

## 🚀 Inicio Rápido

### Requisitos Previos

- Python 3.8+
- pip
- Micrófono y altavoces

### Instalación

1. **Clonar el repositorio**

   ```bash
   git clone <repository-url>
   cd Cortana
   ```

2. **Instalar dependencias**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar APIs**

   - Copia `config/config_example.txt` a `.env`
   - Agrega tus claves de API:
     - Gemini AI API Key
     - Weather API Key (weatherapi.com)
     - News API Key (newsapi.org)
     - Spotify API Keys (opcional)

4. **Inicializar base de datos**

   ```bash
   python utils/init_database.py
   ```

5. **Ejecutar el asistente**
   ```bash
   python src/angie_advanced.py
   ```

## ✨ Características Principales

### 🎯 Funcionalidades Básicas

- **Reconocimiento de voz** en español
- **Síntesis de voz** con respuestas naturales
- **Interfaz gráfica** moderna con CustomTkinter
- **Chat con IA** usando Google Gemini

### 🌟 Funcionalidades Avanzadas

- **Sistema de notas** con base de datos SQLite
- **Información del clima** en tiempo real
- **Noticias** por categorías
- **Búsquedas en Wikipedia**
- **Capturas de pantalla**
- **Información del sistema**
- **Recordatorios y tareas**
- **Integración con Spotify**

### 🧠 Machine Learning

- **Modelo LSTM** para clasificación de comandos
- **Modelo RNN** para procesamiento de lenguaje
- **Entrenamiento personalizable**
- **Visualización de métricas**

## 🛠️ Scripts Útiles

### Verificación del Sistema

```bash
python utils/check_config.py       # Verificar configuración
```

### Entrenamiento de Modelos

```bash
python models/run_lstm_training.py # Entrenar modelo LSTM
python models/entrenar_rnn.py      # Entrenar modelo RNN
python utils/visualize_training.py # Visualizar entrenamiento
```

### Demos y Pruebas

```bash
python demos/demo_clima.py         # Demo del clima
python demos/demo_noticias.py      # Demo de noticias
python tests/test_voice.py         # Probar reconocimiento de voz
```

## 📖 Documentación Detallada

- **[Documentación LSTM](docs/README_LSTM.md)** - Guía completa del modelo LSTM
- **[Sistema de Notas](docs/README_NOTAS.md)** - Funcionalidades de notas
- **[API de Noticias](docs/README_NOTICIAS.md)** - Configuración de noticias
- **[API del Clima](docs/README_WEATHERAPI.md)** - Configuración del clima

## 🔧 Configuración

### Variables de Entorno (.env)

```env
GEMINI_API_KEY=tu_gemini_api_key
WEATHER_API_KEY=tu_weather_api_key
NEWS_API_KEY=tu_news_api_key
DEFAULT_CITY=tu_ciudad
spoty_client_id=tu_spotify_client_id
spoty_client_secret=tu_spotify_client_secret
```

### Comandos de Voz Soportados

- "Angie, ¿qué clima hace?"
- "Angie, reproduce música en Spotify"
- "Angie, toma una nota"
- "Angie, ¿qué noticias hay?"
- "Angie, busca información sobre..."
- "Angie, ¿qué hora es?"
- "Angie, toma una captura"

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👨‍💻 Autor

Desarrollado con ❤️ por [Tu Nombre]

## 🔗 Enlaces Útiles

- [Google Gemini AI](https://ai.google.dev/)
- [Weather API](https://www.weatherapi.com/)
- [News API](https://newsapi.org/)
- [Spotify Web API](https://developer.spotify.com/documentation/web-api/)
