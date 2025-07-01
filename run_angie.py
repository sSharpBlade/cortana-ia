#!/usr/bin/env python3
"""
Script principal para ejecutar Angie Advanced
Ejecutar desde el directorio raíz del proyecto
"""

import os
import sys

# Añadir el directorio del proyecto al path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Cambiar al directorio del proyecto
os.chdir(project_root)

# Importar y ejecutar el asistente
try:
    from src.angie_advanced import AngieAdvanced
    
    if __name__ == "__main__":
        print("🎤 Iniciando Angie Advanced...")
        print("📁 Directorio de trabajo:", os.getcwd())
        
        # Verificar archivos necesarios
        required_files = [
            'data/angie_data.db',
            'src/angie_advanced.py',
            'requirements.txt'
        ]
        
        missing_files = []
        for file_path in required_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
        
        if missing_files:
            print("❌ Archivos faltantes:")
            for file_path in missing_files:
                print(f"   - {file_path}")
            print("\n💡 Asegúrate de ejecutar este script desde el directorio raíz del proyecto")
            print("💡 Si faltan archivos de datos, ejecuta: python utils/init_database.py")
            sys.exit(1)
        
        # Crear instancia y ejecutar
        asistente = AngieAdvanced()
        asistente.run()
        
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("💡 Asegúrate de instalar las dependencias: pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error al iniciar Angie: {e}")
    sys.exit(1)
