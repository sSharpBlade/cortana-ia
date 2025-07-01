# 📝 Sistema de Notas de Angie Advanced

## Descripción General

El sistema de notas de Angie Advanced ha sido completamente mejorado para ofrecer una experiencia completa de gestión de notas con:

- **Almacenamiento en base de datos SQLite**
- **Interfaz gráfica intuitiva**
- **Comandos de voz inteligentes**
- **Búsqueda avanzada**
- **Lectura de notas por voz**
- **Edición y eliminación de notas**

## 🚀 Características Principales

### ✨ Funcionalidades Disponibles

1. **Crear Notas**

   - Interfaz gráfica con campos para título y contenido
   - Guardado automático con fecha y hora
   - Validación de contenido

2. **Visualizar Notas**

   - Vista de todas las notas en formato de lista
   - Preview del contenido de cada nota
   - Ordenación por fecha de modificación

3. **Búsqueda de Notas**

   - Búsqueda por título y contenido
   - Comando de voz inteligente
   - Resultados instantáneos

4. **Lectura por Voz**

   - Lectura de notas individuales
   - Lectura de notas recientes
   - Resumen de notas disponibles

5. **Edición de Notas**

   - Edición completa de título y contenido
   - Actualización automática de fecha de modificación
   - Confirmación de cambios

6. **Eliminación de Notas**

   - Confirmación antes de eliminar
   - Actualización automática de la vista
   - Mensaje de confirmación

7. **Funciones Adicionales**
   - Copia de contenido al portapapeles
   - Contador de notas
   - Ayuda integrada

## 🗣️ Comandos de Voz

### Comandos Básicos

- `"crear nota"` / `"nueva nota"` / `"tomar nota"` - Abre la ventana para crear una nueva nota
- `"ver notas"` / `"mostrar notas"` / `"mis notas"` - Muestra todas las notas guardadas

### Comandos de Búsqueda

- `"buscar nota [término]"` - Busca notas que contengan el término especificado
- Ejemplo: `"buscar nota compras"`

### Comandos de Consulta

- `"cuántas notas"` / `"resumen de notas"` - Muestra el número total de notas y las más recientes
- `"leer notas"` - Lee en voz alta las 3 notas más recientes

### Comandos de Ayuda

- `"ayuda notas"` / `"ayuda de notas"` - Muestra la ayuda completa del sistema

## 💬 Comandos de Texto

Todos los comandos de voz también funcionan como comandos de texto en el chat:

- `crear nota`
- `ver notas`
- `buscar nota término`
- `cuántas notas`
- `leer notas`
- `ayuda notas`

## 🖱️ Interfaz Gráfica

### Botones Principales

- **📝 Nueva Nota** - Crear una nueva nota
- **📚 Ver Notas** - Ver todas las notas guardadas

### Acciones en Cada Nota

- **🔊 Leer** - Escuchar la nota en voz alta
- **✏️ Editar** - Modificar título y contenido
- **🗑️ Eliminar** - Eliminar la nota (con confirmación)
- **📋 Copiar** - Copiar contenido al portapapeles

## 🗄️ Estructura de Base de Datos

```sql
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_date TEXT DEFAULT CURRENT_TIMESTAMP,
    modified_date TEXT DEFAULT CURRENT_TIMESTAMP
);
```

## 🧪 Pruebas y Validación

### Script de Pruebas

Ejecuta `test_notes_system.py` para validar todas las funcionalidades:

```bash
python test_notes_system.py
```

### Casos de Prueba

1. **Conexión a base de datos** - Verifica que la tabla notes existe
2. **Creación de notas** - Inserta notas de ejemplo
3. **Búsqueda** - Prueba búsquedas por diferentes términos
4. **Resumen** - Genera estadísticas de notas
5. **Comandos de voz** - Lista todos los comandos disponibles

## 📋 Ejemplos de Uso

### Crear una Nueva Nota

1. Di `"crear nota"` o haz clic en **📝 Nueva Nota**
2. Ingresa un título (opcional)
3. Escribe el contenido
4. Haz clic en **Guardar Nota**

### Buscar Notas

1. Di `"buscar nota compras"` para buscar notas sobre compras
2. O usa el comando de texto: `buscar nota compras`

### Leer Notas por Voz

1. Di `"leer notas"` para escuchar las 3 notas más recientes
2. O en la vista de notas, haz clic en **🔊 Leer** en cualquier nota

### Ver Resumen

1. Di `"cuántas notas"` para escuchar el resumen
2. Incluye el número total y las notas más recientes

## 🛠️ Solución de Problemas

### Problemas Comunes

1. **La base de datos no existe**

   - Solución: Ejecuta Angie Advanced al menos una vez para crear la base de datos

2. **Error al guardar notas**

   - Verifica que tienes permisos de escritura en el directorio
   - Asegúrate de que la base de datos no esté en uso por otro proceso

3. **Comandos de voz no funcionan**

   - Verifica que el micrófono esté funcionando
   - Habla claramente y espera a que termine el comando anterior

4. **Error de importación pyperclip**
   - Instala las dependencias: `pip install -r requirements.txt`

### Logs y Depuración

Los errores se muestran en:

- Chat de la interfaz gráfica
- Mensajes de voz cuando es apropiado
- Ventanas emergentes para errores críticos

## 🔧 Mantenimiento

### Respaldo de Notas

La base de datos `angie_data.db` contiene todas las notas. Haz respaldos regulares de este archivo.

### Limpieza de Base de Datos

```sql
-- Eliminar notas antiguas (opcional)
-- DELETE FROM notes WHERE created_date < '2024-01-01';

-- Compactar base de datos
-- VACUUM;
```

## 📈 Mejoras Futuras

### Características Planeadas

- [ ] Categorías y etiquetas para notas
- [ ] Sincronización con servicios en la nube
- [ ] Formato de texto enriquecido (markdown)
- [ ] Attachments y multimedia
- [ ] Recordatorios basados en notas
- [ ] Exportación a diferentes formatos

### Integraciones Posibles

- [ ] Google Drive / OneDrive
- [ ] Evernote / Notion
- [ ] Servicios de OCR para imágenes
- [ ] Transcripción automática de voz

## 🤝 Contribución

Si encuentras bugs o tienes sugerencias de mejora:

1. Documenta el problema claramente
2. Incluye pasos para reproducir el error
3. Proporciona logs o mensajes de error
4. Sugiere soluciones si es posible

## 📞 Soporte

Para obtener ayuda adicional:

- Usa el comando `"ayuda notas"` en Angie
- Ejecuta `test_notes_system.py` para diagnósticos
- Revisa esta documentación para casos de uso específicos

---

**Fecha de última actualización:** 2025  
**Versión del Sistema:** Angie Advanced v2.0+  
**Compatibilidad:** Windows, Linux, macOS
