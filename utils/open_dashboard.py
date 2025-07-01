#!/usr/bin/env python3
"""
Script para abrir automáticamente el dashboard HTML
"""

import webbrowser
import os
import sys

def open_dashboard():
    """Abrir el dashboard HTML en el navegador"""
    
    # Ruta del archivo HTML
    dashboard_path = os.path.join('training_plots', 'dashboard.html')
    
    # Verificar si existe el archivo
    if not os.path.exists(dashboard_path):
        print("❌ No se encontró el archivo dashboard.html")
        print("💡 Ejecuta primero: python generate_sample_plots.py")
        return False
    
    # Obtener ruta absoluta
    abs_path = os.path.abspath(dashboard_path)
    
    # Convertir a URL de archivo
    file_url = f"file:///{abs_path.replace(os.sep, '/')}"
    
    print("🌐 Abriendo dashboard HTML...")
    print(f"📁 Archivo: {abs_path}")
    print(f"🔗 URL: {file_url}")
    
    try:
        # Abrir en el navegador predeterminado
        webbrowser.open(file_url)
        print("✅ Dashboard abierto en el navegador")
        return True
    except Exception as e:
        print(f"❌ Error abriendo dashboard: {e}")
        print("\n💡 Alternativas:")
        print("   1. Abre manualmente: training_plots/dashboard.html")
        print("   2. Copia y pega esta URL en tu navegador:")
        print(f"      {file_url}")
        return False

def list_html_files():
    """Listar todos los archivos HTML disponibles"""
    training_plots_dir = 'training_plots'
    
    if not os.path.exists(training_plots_dir):
        print("❌ No existe la carpeta training_plots")
        print("💡 Ejecuta: python generate_sample_plots.py")
        return
    
    html_files = []
    for file in os.listdir(training_plots_dir):
        if file.endswith('.html'):
            html_files.append(file)
    
    if not html_files:
        print("❌ No se encontraron archivos HTML")
        print("💡 Ejecuta: python generate_sample_plots.py")
        return
    
    print("📁 Archivos HTML disponibles:")
    for i, file in enumerate(html_files, 1):
        file_path = os.path.join(training_plots_dir, file)
        abs_path = os.path.abspath(file_path)
        print(f"   {i}. {file}")
        print(f"      Ruta: {abs_path}")
        print(f"      URL: file:///{abs_path.replace(os.sep, '/')}")
        print()

def main():
    """Función principal"""
    print("🌐 Abridor de Dashboard LSTM")
    print("=" * 40)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--list":
            list_html_files()
            return
        elif sys.argv[1] == "--help":
            print("Uso:")
            print("  python open_dashboard.py          # Abrir dashboard principal")
            print("  python open_dashboard.py --list   # Listar archivos HTML")
            print("  python open_dashboard.py --help   # Mostrar ayuda")
            return
    
    # Abrir dashboard principal
    success = open_dashboard()
    
    if success:
        print("\n🎉 ¡Dashboard abierto exitosamente!")
        print("📊 Puedes ver todas las visualizaciones del entrenamiento LSTM")
    else:
        print("\n💡 Si tienes problemas:")
        print("   1. Asegúrate de que el archivo existe")
        print("   2. Ejecuta: python generate_sample_plots.py")
        print("   3. Abre manualmente el archivo en tu navegador")

if __name__ == "__main__":
    main() 