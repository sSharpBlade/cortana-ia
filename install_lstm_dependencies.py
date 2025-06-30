#!/usr/bin/env python3
"""
Script para instalar dependencias del sistema LSTM
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
    print("🚀 Instalando dependencias para el sistema LSTM...")
    print("=" * 60)
    
    # Lista de dependencias principales
    dependencies = [
        "tensorflow>=2.10.0",
        "numpy>=1.21.0", 
        "pandas>=1.3.0",
        "matplotlib>=3.5.0",
        "seaborn>=0.11.0",
        "scikit-learn>=1.0.0"
    ]
    
    # Dependencias opcionales para mejor rendimiento
    optional_dependencies = [
        "tensorflow-gpu",  # Para GPU si está disponible
        "plotly",          # Para visualizaciones interactivas
        "jupyter"          # Para notebooks
    ]
    
    print("📋 Dependencias principales:")
    success_count = 0
    
    for dep in dependencies:
        if install_package(dep):
            success_count += 1
    
    print(f"\n✅ {success_count}/{len(dependencies)} dependencias principales instaladas")
    
    print("\n📋 Dependencias opcionales (para mejor rendimiento):")
    print("💡 Estas son opcionales pero recomendadas:")
    
    for dep in optional_dependencies:
        try:
            print(f"📦 Intentando instalar {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✅ {dep} instalado exitosamente")
        except subprocess.CalledProcessError:
            print(f"⚠️  {dep} no se pudo instalar (opcional)")
    
    print("\n" + "=" * 60)
    print("🎉 Instalación completada!")
    print("\n📊 Para verificar la instalación:")
    print("   python run_lstm_training.py --example")
    print("\n🚀 Para entrenar el modelo:")
    print("   python run_lstm_training.py")
    
    # Verificar instalación
    print("\n🔍 Verificando instalación...")
    try:
        import tensorflow as tf
        print(f"✅ TensorFlow {tf.__version__} instalado")
        
        import numpy as np
        print(f"✅ NumPy {np.__version__} instalado")
        
        import pandas as pd
        print(f"✅ Pandas {pd.__version__} instalado")
        
        import matplotlib
        print(f"✅ Matplotlib {matplotlib.__version__} instalado")
        
        import seaborn as sns
        print(f"✅ Seaborn instalado")
        
        import sklearn
        print(f"✅ Scikit-learn {sklearn.__version__} instalado")
        
        print("\n🎯 ¡Todas las dependencias están listas!")
        
    except ImportError as e:
        print(f"❌ Error verificando dependencias: {e}")
        print("💡 Ejecuta manualmente: pip install -r requirements.txt")

if __name__ == "__main__":
    main() 