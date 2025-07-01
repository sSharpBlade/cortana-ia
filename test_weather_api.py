#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para la funcionalidad de clima con WeatherAPI
"""

import os
import requests
from dotenv import load_dotenv

def test_weather_api():
    """Prueba la conexión con WeatherAPI"""
    load_dotenv()
    
    weather_api_key = os.getenv("WEATHER_API_KEY")
    default_city = os.getenv("DEFAULT_CITY", "Madrid")
    
    print("🌤️  Prueba de WeatherAPI")
    print("=" * 50)
    
    # Verificar que la API key esté configurada
    if not weather_api_key or weather_api_key == "your_weatherapi_key_here":
        print("❌ ERROR: API key no configurada")
        print("Por favor, configura WEATHER_API_KEY en el archivo .env")
        return False
    
    print(f"✅ API Key encontrada: {weather_api_key[:10]}...")
    print(f"🏙️  Ciudad por defecto: {default_city}")
    
    # Probar consulta de clima
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={default_city}&lang=es"
        print(f"🔗 URL de prueba: {url}")
        
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if response.status_code == 200:
            temp = data['current']['temp_c']
            condition = data['current']['condition']['text']
            humidity = data['current']['humidity']
            wind_speed = data['current']['wind_kph']
            feels_like = data['current']['feelslike_c']
            location = data['location']['name']
            country = data['location']['country']
            
            print("\n✅ ¡Conexión exitosa!")
            print("📊 Datos obtenidos:")
            print(f"   📍 Ubicación: {location}, {country}")
            print(f"   🌡️  Temperatura: {temp}°C")
            print(f"   🌤️  Condición: {condition}")
            print(f"   🤗 Sensación térmica: {feels_like}°C")
            print(f"   💧 Humedad: {humidity}%")
            print(f"   💨 Viento: {wind_speed} km/h")
            
            return True
        else:
            print(f"❌ Error HTTP {response.status_code}")
            print(f"Respuesta: {data}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ ERROR: Timeout en la conexión")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: No se pudo conectar a WeatherAPI")
        print("Verifica tu conexión a internet")
        return False
    except Exception as e:
        print(f"❌ ERROR inesperado: {str(e)}")
        return False

def test_cities():
    """Prueba consultas para diferentes ciudades"""
    load_dotenv()
    weather_api_key = os.getenv("WEATHER_API_KEY")
    
    if not weather_api_key or weather_api_key == "your_weatherapi_key_here":
        print("❌ Saltando prueba de ciudades: API key no configurada")
        return
    
    cities = ["Barcelona", "París", "Londres", "Nueva York", "Tokio"]
    print(f"\n🌍 Probando ciudades internacionales...")
    print("=" * 50)
    
    for city in cities:
        try:
            url = f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}&lang=es"
            response = requests.get(url, timeout=5)
            data = response.json()
            
            if response.status_code == 200:
                temp = data['current']['temp_c']
                condition = data['current']['condition']['text']
                location = data['location']['name']
                country = data['location']['country']
                print(f"✅ {location}, {country}: {temp}°C, {condition}")
            else:
                print(f"❌ {city}: Error {response.status_code}")
                
        except Exception as e:
            print(f"❌ {city}: Error - {str(e)}")

if __name__ == "__main__":
    print("🧪 Iniciando pruebas de WeatherAPI...")
    print()
    
    # Prueba básica
    success = test_weather_api()
    
    if success:
        # Prueba de ciudades internacionales
        test_cities()
        
        print("\n🎉 ¡Todas las pruebas completadas!")
        print("Tu asistente está listo para usar WeatherAPI.")
    else:
        print("\n❌ Hay problemas con la configuración.")
        print("Revisa el archivo README_WEATHERAPI.md para más información.")
