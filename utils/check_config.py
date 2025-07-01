#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificador de Configuración - Angie Advanced
============================================

Este script verifica la configuración de API keys y ayuda a configurarlas.

Uso: python check_config.py
"""

import os
from dotenv import load_dotenv
import requests

def check_configuration():
    """Verificar la configuración de API keys"""
    
    print("🔧 Verificador de Configuración - Angie Advanced")
    print("=" * 55)
    print()
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Verificar archivo .env
    if not os.path.exists('.env'):
        print("❌ Archivo .env no encontrado")
        print()
        print("💡 Solución:")
        print("1. Copia el archivo .env.example como .env")
        print("2. Edita el archivo .env con tus API keys")
        print()
        return False
    
    print("✅ Archivo .env encontrado")
    print()
    
    # Verificar API keys
    apis_status = {}
    
    # NewsAPI
    news_api_key = os.getenv("NEWS_API_KEY")
    if news_api_key and news_api_key != "tu_news_api_key_aqui":
        try:
            response = requests.get(f"https://newsapi.org/v2/top-headlines?country=es&apiKey={news_api_key}", timeout=5)
            if response.status_code == 200:
                apis_status["NewsAPI"] = {"status": "✅", "message": "Configurada correctamente"}
            elif response.status_code == 401:
                apis_status["NewsAPI"] = {"status": "❌", "message": "API key inválida"}
            else:
                apis_status["NewsAPI"] = {"status": "⚠️", "message": f"Error: {response.status_code}"}
        except:
            apis_status["NewsAPI"] = {"status": "⚠️", "message": "Error de conexión"}
    else:
        apis_status["NewsAPI"] = {"status": "❌", "message": "No configurada"}
    
    # Gemini API
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if gemini_api_key and gemini_api_key != "tu_gemini_api_key_aqui":
        apis_status["Gemini"] = {"status": "✅", "message": "Configurada"}
    else:
        apis_status["Gemini"] = {"status": "❌", "message": "No configurada"}
    
    # Weather API
    weather_api_key = os.getenv("WEATHER_API_KEY")
    if weather_api_key and weather_api_key != "tu_weather_api_key_aqui":
        try:
            response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q=Madrid", timeout=5)
            if response.status_code == 200:
                apis_status["WeatherAPI"] = {"status": "✅", "message": "Configurada correctamente"}
            elif response.status_code == 401:
                apis_status["WeatherAPI"] = {"status": "❌", "message": "API key inválida"}
            else:
                apis_status["WeatherAPI"] = {"status": "⚠️", "message": f"Error: {response.status_code}"}
        except:
            apis_status["WeatherAPI"] = {"status": "⚠️", "message": "Error de conexión"}
    else:
        apis_status["WeatherAPI"] = {"status": "❌", "message": "No configurada"}
    
    # Mostrar resultados
    print("📊 Estado de las APIs:")
    print("-" * 30)
    for api_name, info in apis_status.items():
        print(f"{info['status']} {api_name}: {info['message']}")
    
    print()
    
    # Funcionalidades disponibles
    print("🎯 Funcionalidades disponibles:")
    print("-" * 35)
    
    if apis_status["NewsAPI"]["status"] == "✅":
        print("✅ Centro de noticias completo")
        print("✅ Comandos de voz para noticias")
        print("✅ Búsqueda personalizada de noticias")
    else:
        print("❌ Noticias (requiere NewsAPI)")
    
    if apis_status["WeatherAPI"]["status"] == "✅":
        print("✅ Información del clima")
    else:
        print("❌ Clima (requiere WeatherAPI)")
    
    if apis_status["Gemini"]["status"] == "✅":
        print("✅ Respuestas de IA avanzadas")
    else:
        print("❌ IA avanzada (requiere Gemini)")
    
    print("✅ Comandos de voz básicos")
    print("✅ Notas y recordatorios")
    print("✅ Búsquedas en Wikipedia")
    print("✅ Información del sistema")
    print("✅ Gestión de tareas")
    
    print()
    
    # Recomendaciones
    if apis_status["NewsAPI"]["status"] != "✅":
        print("💡 Para activar las noticias:")
        print("1. Ve a https://newsapi.org/")
        print("2. Crea una cuenta gratuita")
        print("3. Copia tu API key al archivo .env")
        print()
    
    if apis_status["WeatherAPI"]["status"] != "✅":
        print("💡 Para activar el clima:")
        print("1. Ve a https://www.weatherapi.com/")
        print("2. Crea una cuenta gratuita")
        print("3. Copia tu API key al archivo .env")
        print()
    
    if apis_status["Gemini"]["status"] != "✅":
        print("💡 Para activar IA avanzada:")
        print("1. Ve a https://makersuite.google.com/app/apikey")
        print("2. Crea una cuenta de Google")
        print("3. Copia tu API key al archivo .env")
        print()
    
    # Estado general
    working_apis = sum(1 for api in apis_status.values() if api["status"] == "✅")
    total_apis = len(apis_status)
    
    print(f"📈 Configuración: {working_apis}/{total_apis} APIs funcionando")
    
    if working_apis == total_apis:
        print("🎉 ¡Configuración perfecta! Todas las funcionalidades están disponibles.")
    elif working_apis >= 1:
        print("👍 ¡Buena configuración! La mayoría de funcionalidades están disponibles.")
    else:
        print("⚠️ Configuración básica. Configura las APIs para más funcionalidades.")
    
    return working_apis > 0

def main():
    """Función principal"""
    try:
        check_configuration()
    except Exception as e:
        print(f"❌ Error al verificar configuración: {e}")
    
    print()
    input("Presiona Enter para continuar...")

if __name__ == "__main__":
    main()
