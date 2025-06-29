# 🎤 Angie - Asistente Virtual Inteligente

Un asistente virtual moderno con interfaz gráfica que combina reconocimiento de voz, inteligencia artificial y múltiples funcionalidades útiles.

## ✨ Características Principales

### 🎯 Funcionalidades Básicas
- **Reconocimiento de voz** en español
- **Síntesis de voz** para respuestas habladas
- **Interfaz gráfica moderna** con CustomTkinter
- **Integración con Google Gemini AI** para respuestas inteligentes

### 🚀 Funcionalidades Avanzadas
- **🎵 Reproducción de música** en YouTube y Spotify
- **🌤️ Información del clima** en tiempo real
- **📰 Noticias actuales** de España
- **🔍 Búsquedas en Wikipedia**
- **📝 Sistema de notas** integrado
- **🖥️ Capturas de pantalla**
- **⏰ Consulta de hora**
- **📊 Historial de comandos**

### 🎨 Interfaz Visual
- **Tema oscuro moderno**
- **Botones de comandos rápidos**
- **Área de chat en tiempo real**
- **Indicadores de estado**
- **Entrada de texto manual**

## 🛠️ Instalación

1. **Clonar el repositorio:**
```bash
git clone <tu-repositorio>
cd AsistenteVirtual
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Configurar API Keys:**
   - Copia `config_example.txt` a `.env`
   - Agrega tus API keys necesarias

## 🔑 API Keys Requeridas

### Obligatoria:
- **GEMINI_API_KEY**: Google Gemini AI (https://makersuite.google.com/app/apikey)

### Opcionales:
- **NEWS_API_KEY**: News API (https://newsapi.org/)
- **WEATHER_API_KEY**: OpenWeatherMap (https://openweathermap.org/api)
- **spoty_client_id & spoty_client_secret**: Spotify (https://developer.spotify.com/)

## 🚀 Uso

### Ejecutar la interfaz visual:
```bash
python angie_assistant.py
```

### Comandos de voz:
- "Angie, reproduce [canción]" - Reproduce música en YouTube
- "Angie, reproduce en spotify [canción]" - Reproduce en Spotify
- "Angie, ¿qué hora es?" - Consulta la hora
- "Angie, ¿cómo está el clima?" - Información del clima
- "Angie, dame las noticias" - Noticias actuales
- "Angie, busca [término]" - Búsqueda en Wikipedia
- "Angie, toma una nota" - Abre editor de notas
- "Angie, toma una captura" - Captura de pantalla
- "Angie, descansa" - Cierra el asistente

### Comandos por texto:
- Usa la barra de entrada de texto para comandos manuales
- Presiona Enter o el botón "Enviar"

## 📁 Estructura del Proyecto

```
AsistenteVirtual/
├── angie_assistant.py      # Asistente principal con interfaz visual
├── version1.py            # Versión anterior (consola)
├── spoty.py              # Módulo de Spotify
├── requirements.txt       # Dependencias
├── config_example.txt    # Ejemplo de configuración
├── historial_comandos.csv # Historial de comandos
└── README.md             # Este archivo
```

## 🎯 Comandos Rápidos

La interfaz incluye botones para acceder rápidamente a:
- 🌤️ Clima
- 📰 Noticias  
- ⏰ Hora
- 🔍 Buscar
- 📝 Notas
- 🖥️ Captura

## 🔧 Personalización

### Cambiar el nombre del asistente:
Edita la línea `self.name = 'angie'` en `angie_assistant.py`

### Agregar nuevas funcionalidades:
1. Crea una nueva función en la clase `AngieAssistant`
2. Agrega el comando en `process_command()`
3. Opcionalmente, agrega un botón en la interfaz

## 📝 Historial

El asistente guarda automáticamente todos los comandos y respuestas en `historial_comandos.csv` con timestamps.

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Puedes:
- Agregar nuevas funcionalidades
- Mejorar la interfaz
- Optimizar el código
- Reportar bugs

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

---

**¡Disfruta usando Angie, tu asistente virtual personal! 🎤✨**
