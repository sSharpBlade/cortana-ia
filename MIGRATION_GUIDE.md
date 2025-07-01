# 🔄 Guía de Migración de Rutas

Este documento contiene las rutas que han cambiado después de la reorganización del proyecto.

## 📋 Cambios de Rutas

### Archivos Principales

| Archivo Original     | Nueva Ubicación          |
| -------------------- | ------------------------ |
| `angie_advanced.py`  | `src/angie_advanced.py`  |
| `angie_assistant.py` | `src/angie_assistant.py` |
| `spoty.py`           | `src/spoty.py`           |
| `version1.py`        | `src/version1.py`        |

### Modelos y Entrenamiento

| Archivo Original         | Nueva Ubicación                 |
| ------------------------ | ------------------------------- |
| `modelo_rnn_comandos.h5` | `models/modelo_rnn_comandos.h5` |
| `tokenizer.pickle`       | `models/tokenizer.pickle`       |
| `angie_lstm_trainer.py`  | `models/angie_lstm_trainer.py`  |
| `entrenar_rnn.py`        | `models/entrenar_rnn.py`        |

### Datos y Base de Datos

| Archivo Original         | Nueva Ubicación               |
| ------------------------ | ----------------------------- |
| `angie_data.db`          | `data/angie_data.db`          |
| `historial_comandos.csv` | `data/historial_comandos.csv` |
| `nota_*.txt`             | `data/nota_*.txt`             |

### Documentación

| Archivo Original               | Nueva Ubicación                     |
| ------------------------------ | ----------------------------------- |
| `README_*.md`                  | `docs/README_*.md`                  |
| `INSTRUCCIONES_LSTM.md`        | `docs/INSTRUCCIONES_LSTM.md`        |
| `MEJORAS_NOTAS_COMPLETADAS.md` | `docs/MEJORAS_NOTAS_COMPLETADAS.md` |

### Utilidades

| Archivo Original   | Nueva Ubicación          |
| ------------------ | ------------------------ |
| `check_config.py`  | `utils/check_config.py`  |
| `init_database.py` | `utils/init_database.py` |
| `install_*.py`     | `utils/install_*.py`     |

## 🔧 Actualizaciones Necesarias en el Código

### 1. Referencias a la Base de Datos

**Antes:**

```python
self.conn = sqlite3.connect('angie_data.db')
```

**Después:**

```python
self.conn = sqlite3.connect('data/angie_data.db')
```

### 2. Referencias al Modelo

**Antes:**

```python
model = load_model('modelo_rnn_comandos.h5')
```

**Después:**

```python
model = load_model('models/modelo_rnn_comandos.h5')
```

### 3. Referencias al Tokenizer

**Antes:**

```python
with open('tokenizer.pickle', 'rb') as handle:
```

**Después:**

```python
with open('models/tokenizer.pickle', 'rb') as handle:
```

### 4. Referencias al Historial

**Antes:**

```python
with open('historial_comandos.csv', mode='a') as file:
```

**Después:**

```python
with open('data/historial_comandos.csv', mode='a') as file:
```

### 5. Referencias a Capturas de Pantalla

**Antes:**

```python
screenshot.save(filename)
```

**Después:**

```python
screenshot.save(f"media/{filename}")
```

## 🚀 Script de Actualización Automática

Puedes usar este script para actualizar automáticamente las rutas en tus archivos:

```python
import os
import re

def update_file_paths(file_path):
    """Actualizar rutas en un archivo específico"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Actualizaciones de rutas
    updates = {
        r"'angie_data\.db'": "'data/angie_data.db'",
        r'"angie_data\.db"': '"data/angie_data.db"',
        r"'historial_comandos\.csv'": "'data/historial_comandos.csv'",
        r'"historial_comandos\.csv"': '"data/historial_comandos.csv"',
        r"'modelo_rnn_comandos\.h5'": "'models/modelo_rnn_comandos.h5'",
        r'"modelo_rnn_comandos\.h5"': '"models/modelo_rnn_comandos.h5"',
        r"'tokenizer\.pickle'": "'models/tokenizer.pickle'",
        r'"tokenizer\.pickle"': '"models/tokenizer.pickle"',
    }

    for old_pattern, new_path in updates.items():
        content = re.sub(old_pattern, new_path, content)

    # Actualizar capturas de pantalla
    content = re.sub(
        r'screenshot\.save\(filename\)',
        'screenshot.save(f"media/{filename}")',
        content
    )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# Ejecutar para todos los archivos Python en src/
for filename in os.listdir('src'):
    if filename.endswith('.py'):
        update_file_paths(f'src/{filename}')
        print(f"Actualizado: src/{filename}")
```

## ⚠️ Notas Importantes

1. **Ejecutar desde el directorio raíz**: Asegúrate de ejecutar todos los scripts desde el directorio raíz del proyecto (`Cortana/`).

2. **Rutas relativas**: Los archivos ahora usan rutas relativas desde el directorio raíz.

3. **Imports**: Si hay imports entre módulos, puede que necesites actualizar el `sys.path` o usar imports relativos.

4. **Variables de entorno**: El archivo `.env` sigue en el directorio raíz.

## 🔍 Verificación

Para verificar que todas las rutas funcionan correctamente:

```bash
# Desde el directorio raíz
python utils/check_config.py
python src/angie_advanced.py
```

Si encuentras errores de rutas, revisa este documento y actualiza las referencias según sea necesario.
