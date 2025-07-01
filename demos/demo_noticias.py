#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo de Funcionalidad de Noticias - Angie Advanced
=================================================

Este script demuestra las capacidades avanzadas de noticias del asistente Angie.

Características implementadas:
- Múltiples categorías de noticias
- Búsqueda personalizada
- Noticias por país
- Interfaz gráfica avanzada
- Funcionalidad de voz
- Compartir noticias
- Resúmenes automáticos

Autor: Angie Advanced Team
Fecha: Julio 2025
"""

import sys
import os
from datetime import datetime

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar la clase principal
from angie_advanced import AngieAdvanced

def demo_news_functionality():
    """Demonstración de las funcionalidades de noticias"""
    
    print("🎤 Demo - Funcionalidad de Noticias - Angie Advanced")
    print("=" * 60)
    print()
    
    # Verificar archivo .env
    if not os.path.exists('.env'):
        print("⚠️ ADVERTENCIA: No se encuentra el archivo .env")
        print("Por favor, crea un archivo .env basado en config_example.txt")
        print("Necesitarás una API key de NewsAPI para usar las noticias")
        print()
        
        respuesta = input("¿Deseas continuar con la demo sin API? (s/n): ")
        if respuesta.lower() != 's':
            return
    
    print("🚀 Iniciando Angie Advanced...")
    
    try:
        # Crear instancia del asistente
        angie = AngieAdvanced()
        
        print("✅ Angie Advanced iniciado correctamente")
        print()
        print("📰 Funcionalidades de Noticias Disponibles:")
        print("-" * 50)
        print("1. 🌍 Noticias generales")
        print("2. 💼 Noticias de negocios")
        print("3. 🎮 Entretenimiento")
        print("4. 💊 Salud")
        print("5. 🔬 Ciencia")
        print("6. ⚽ Deportes")
        print("7. 💻 Tecnología")
        print("8. 🔍 Búsqueda personalizada")
        print("9. 🌏 Noticias internacionales")
        print()
        
        print("🎤 Comandos de Voz Soportados:")
        print("-" * 35)
        print("• 'noticias' - Abrir centro de noticias")
        print("• 'noticias rápidas' - Resumen de voz")
        print("• 'noticias de deportes' - Noticias deportivas")
        print("• 'noticias de tecnología' - Noticias tech")
        print("• 'noticias de ciencia' - Noticias científicas")
        print("• 'noticias de salud' - Noticias de salud")
        print("• 'noticias de negocios' - Noticias económicas")
        print()
        
        print("💡 Características Avanzadas:")
        print("-" * 32)
        print("✓ Interfaz gráfica moderna")
        print("✓ Múltiples fuentes de noticias")
        print("✓ Filtros por categoría y país")
        print("✓ Búsqueda personalizada")
        print("✓ Lectura en voz alta")
        print("✓ Compartir noticias")
        print("✓ Resúmenes automáticos")
        print("✓ Enlaces directos a artículos")
        print()
        
        # Mostrar comandos de prueba
        print("🧪 Comandos de Prueba:")
        print("-" * 22)
        print("Puedes probar estos comandos cuando el asistente esté activo:")
        print()
        
        comandos_prueba = [
            "noticias",
            "noticias rápidas",
            "noticias de deportes",
            "noticias de tecnología",
            "noticias de ciencia"
        ]
        
        for i, comando in enumerate(comandos_prueba, 1):
            print(f"{i}. '{comando}'")
        
        print()
        print("🔧 Configuración:")
        print("-" * 16)
        
        # Verificar configuración de API
        news_api_key = os.getenv("NEWS_API_KEY")
        if news_api_key:
            print("✅ API de NewsAPI configurada")
        else:
            print("❌ API de NewsAPI no configurada")
            print("   Obtén tu API key gratuita en: https://newsapi.org/")
        
        print()
        print("🎯 La interfaz gráfica se abrirá ahora...")
        print("   Usa el botón '📰 Noticias' o activa el micrófono")
        print("   y di 'noticias' para probar la funcionalidad")
        print()
        
        # Ejecutar la aplicación
        angie.root.mainloop()
        
    except Exception as e:
        print(f"❌ Error al iniciar Angie Advanced: {str(e)}")
        print()
        print("💡 Posibles soluciones:")
        print("1. Verifica que todas las dependencias estén instaladas:")
        print("   pip install -r requirements.txt")
        print("2. Configura tu archivo .env con las API keys necesarias")
        print("3. Verifica tu conexión a internet")

def main():
    """Función principal"""
    demo_news_functionality()

if __name__ == "__main__":
    main()
