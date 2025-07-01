# 📰 Funcionalidad de Noticias - Angie Advanced

## Descripción General

La funcionalidad de noticias de Angie Advanced proporciona un sistema completo y avanzado para mantenerte informado con las últimas noticias de múltiples fuentes y categorías.

## 🌟 Características Principales

### 📱 Interfaz Gráfica Moderna

- Centro de noticias con diseño intuitivo
- Tarjetas de noticias con información detallada
- Controles para filtrar por categoría y país
- Búsqueda personalizada de noticias

### 🎤 Comandos de Voz Inteligentes

- `"noticias"` - Abre el centro de noticias completo
- `"noticias rápidas"` - Resumen de voz de noticias principales
- `"noticias de deportes"` - Noticias deportivas específicas
- `"noticias de tecnología"` - Últimas noticias tecnológicas
- `"noticias de ciencia"` - Noticias científicas
- `"noticias de salud"` - Noticias de salud y medicina
- `"noticias de negocios"` - Noticias económicas y de negocios
- `"noticias de entretenimiento"` - Noticias de entretenimiento

### 🌍 Múltiples Fuentes y Países

- Noticias de España (es)
- Noticias de Estados Unidos (us)
- Noticias de Reino Unido (gb)
- Noticias de Francia (fr)
- Noticias de Alemania (de)
- Noticias de Italia (it)
- Noticias de México (mx)
- Noticias de Argentina (ar)

### 📂 Categorías Disponibles

- **General**: Noticias generales
- **Business**: Negocios y economía
- **Entertainment**: Entretenimiento
- **Health**: Salud y medicina
- **Science**: Ciencia y tecnología
- **Sports**: Deportes
- **Technology**: Tecnología

## 🚀 Configuración

### 1. Obtener API Key de NewsAPI

1. Visita [NewsAPI.org](https://newsapi.org/)
2. Crea una cuenta gratuita
3. Obtén tu API key gratuita

### 2. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# API Key de NewsAPI
NEWS_API_KEY=tu_api_key_aqui

# Otras configuraciones opcionales
GEMINI_API_KEY=tu_gemini_api_key
WEATHER_API_KEY=tu_weather_api_key
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

## 🎯 Uso

### Desde la Interfaz Gráfica

1. Ejecuta `python angie_advanced.py`
2. Haz clic en el botón "📰 Noticias"
3. Usa los controles para filtrar y buscar noticias

### Desde Comandos de Voz

1. Activa el micrófono con "🎤 Activar Angie"
2. Di cualquier comando de noticias
3. Escucha la respuesta o ve la interfaz gráfica

### Demo Específica

```bash
python demo_noticias.py
```

## 🔧 Funcionalidades Avanzadas

### 🔊 Lectura en Voz Alta

- Cada noticia puede ser leída en voz alta
- Resúmenes automáticos de noticias principales
- Síntesis de voz natural

### 📤 Compartir Noticias

- Copia noticias al portapapeles
- Comparte títulos y enlaces
- Integración con el sistema

### 🔍 Búsqueda Personalizada

- Busca noticias sobre temas específicos
- Resultados ordenados por relevancia
- Filtros por fecha y fuente

### 🎨 Interfaz Visual

- Diseño moderno con CustomTkinter
- Modo oscuro para mejor experiencia
- Tarjetas de noticias con información completa
- Botones de acción integrados

## 📊 Estructura de Datos

### Información de Noticia

Cada noticia incluye:

- **Título**: Título principal de la noticia
- **Descripción**: Resumen de la noticia
- **Fuente**: Medio de comunicación
- **Fecha**: Fecha de publicación
- **URL**: Enlace al artículo completo
- **Imagen**: URL de imagen (si disponible)

## 🛠️ Personalización

### Modificar Categorías

Puedes agregar más categorías editando el archivo `angie_advanced.py`:

```python
# En la función show_news_window
values=["general", "business", "entertainment",
        "health", "science", "sports", "technology", "nueva_categoria"]
```

### Cambiar Países Predeterminados

Modifica la lista de países en el menú desplegable:

```python
# En la función show_news_window
values=["es", "us", "gb", "fr", "de", "it", "mx", "ar", "nuevo_pais"]
```

### Personalizar Comandos de Voz

Agrega nuevos comandos en la función `process_command`:

```python
elif "mi_comando_personalizado" in command:
    self.get_quick_news_summary("mi_categoria")
```

## 🐛 Solución de Problemas

### Error de API Key

- Verifica que tu API key esté correctamente configurada en `.env`
- Asegúrate de que la API key no haya expirado
- Revisa los límites de tu plan de NewsAPI

### Error de Conexión

- Verifica tu conexión a internet
- Comprueba que NewsAPI esté disponible
- Revisa las configuraciones de firewall

### Error de Dependencias

```bash
pip install --upgrade -r requirements.txt
```

## 📈 Límites de la API Gratuita

### NewsAPI Gratuito

- 1,000 solicitudes por mes
- Noticias de hasta 1 mes de antigüedad
- Acceso a fuentes principales

### Recomendaciones

- Usa la funcionalidad con moderación
- Considera actualizar a plan premium para uso intensivo
- Implementa cache local para reducir llamadas a la API

## 🔄 Actualizaciones Futuras

### Próximas Características

- [ ] Cache local de noticias
- [ ] Notificaciones push
- [ ] Integración con redes sociales
- [ ] Análisis de sentimientos
- [ ] Resúmenes con IA
- [ ] Traducciones automáticas
- [ ] Modo offline

## 📞 Soporte

Si encuentras problemas:

1. Revisa este README
2. Ejecuta `python demo_noticias.py` para diagnóstico
3. Verifica tu configuración de API keys
4. Consulta los logs de error en la consola

## 📜 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

---

**Desarrollado con ❤️ por el equipo de Angie Advanced**
