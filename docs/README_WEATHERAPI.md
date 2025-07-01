# Configuración del Clima con WeatherAPI

## Descripción

El asistente virtual Angie ahora utiliza WeatherAPI.com para obtener información meteorológica más precisa y detallada.

## Configuración

### 1. Obtener API Key

1. Visita [WeatherAPI.com](https://www.weatherapi.com)
2. Crea una cuenta gratuita
3. Obtén tu API key del dashboard

### 2. Configurar Variables de Entorno

Edita el archivo `.env` y reemplaza `your_weatherapi_key_here` con tu clave real:

```env
WEATHER_API_KEY=tu_clave_real_aqui
DEFAULT_CITY=Madrid
```

## Funcionalidades

### Comandos de Clima Disponibles

#### Clima de la ciudad por defecto:

- "¿Qué clima hay?"
- "Dime el tiempo"
- "¿Cómo está el clima?"

#### Clima de una ciudad específica:

- "¿Qué clima hay en Barcelona?"
- "Dime el tiempo de París"
- "¿Cómo está el clima en Londres?"
- "Clima de Nueva York"
- "Tiempo en Tokio"

### Información Proporcionada

- Temperatura actual en Celsius
- Descripción del clima (soleado, nublado, lluvia, etc.)
- Sensación térmica
- Humedad relativa
- Velocidad del viento en km/h
- Nombre completo de la ubicación y país

### Ejemplo de Respuesta

```
"En Madrid, España: 22°C, Parcialmente nublado. Sensación térmica: 24°C, humedad: 65%, viento: 12 km/h"
```

## Características Técnicas

### Mejoras Implementadas

- **Manejo de errores mejorado**: Mensajes de error más descriptivos
- **Soporte multiidioma**: Respuestas en español
- **Información detallada**: Más datos meteorológicos que la versión anterior
- **Búsqueda inteligente de ciudades**: Reconoce ciudades internacionales
- **Configuración flexible**: Ciudad por defecto configurable

### Limitaciones

- Plan gratuito de WeatherAPI: 1,000,000 consultas por mes
- Requiere conexión a internet
- Depende de la disponibilidad del servicio WeatherAPI

## Solución de Problemas

### Error: "Ciudad no encontrada"

- Verifica que el nombre de la ciudad esté escrito correctamente
- Prueba con nombres en inglés para ciudades internacionales
- Incluye el país si hay ambigüedad (ej: "París Francia")

### Error: "No pude obtener el clima"

- Verifica tu conexión a internet
- Confirma que la API key sea válida
- Revisa que no hayas excedido el límite de consultas

### Error de API Key

- Verifica que la variable `WEATHER_API_KEY` esté configurada correctamente en `.env`
- Asegúrate de que la API key sea válida y activa
- Revisa que no haya espacios extra en la configuración

## Archivos Modificados

- `angie_advanced_temp.py`
- `angie_advanced.py`
- `angie_assistant.py`
- `.env`
- `requirements.txt`

## Migración desde OpenWeatherMap

Los archivos han sido actualizados automáticamente para usar WeatherAPI en lugar de OpenWeatherMap. Solo necesitas:

1. Obtener una API key de WeatherAPI
2. Actualizar el archivo `.env`
3. Reiniciar el asistente
