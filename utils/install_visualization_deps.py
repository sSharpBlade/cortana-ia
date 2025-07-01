#!/usr/bin/env python3
"""
Script para instalar dependencias de visualización
"""

import subprocess
import sys
import os

def install_package(package):
    """Instalar un paquete usando pip"""
    try:
        print(f"📦 Instalando {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} instalado exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando {package}: {e}")
        return False

def main():
    """Función principal de instalación"""
    print("🎨 Instalando dependencias para visualizaciones...")
    print("=" * 60)
    
    # Dependencias para visualizaciones
    visualization_deps = [
        "matplotlib>=3.5.0",
        "seaborn>=0.11.0", 
        "numpy>=1.21.0"
    ]
    
    print("📋 Dependencias de visualización:")
    success_count = 0
    
    for dep in visualization_deps:
        if install_package(dep):
            success_count += 1
    
    print(f"\n✅ {success_count}/{len(visualization_deps)} dependencias instaladas")
    
    # Verificar instalación
    print("\n🔍 Verificando instalación...")
    try:
        import matplotlib
        print(f"✅ Matplotlib {matplotlib.__version__} instalado")
        
        import seaborn as sns
        print(f"✅ Seaborn instalado")
        
        import numpy as np
        print(f"✅ NumPy {np.__version__} instalado")
        
        print("\n🎯 ¡Todas las dependencias están listas!")
        print("\n📊 Para ver las visualizaciones:")
        print("   python visualize_training.py")
        
    except ImportError as e:
        print(f"❌ Error verificando dependencias: {e}")
        print("💡 Ejecuta manualmente: pip install matplotlib seaborn numpy")

if __name__ == "__main__":
    main() 