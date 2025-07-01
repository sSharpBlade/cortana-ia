#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueba de API de Noticias - Angie Advanced
==========================================

Este script prueba diferentes categorías de noticias para diagnosticar problemas.

Uso: python test_news_api.py
"""

import os
import requests
from dotenv import load_dotenv

def test_news_api():
    """Probar diferentes categorías de noticias"""
    
    print("🧪 Prueba de API de Noticias - Angie Advanced")
    print("=" * 50)
    print()
    
    # Cargar variables de entorno
    load_dotenv()
    
    news_api_key = os.getenv("NEWS_API_KEY")
    
    if not news_api_key or news_api_key == "tu_news_api_key_aqui":
        print("❌ API key de noticias no configurada")
        print("Configura NEWS_API_KEY en el archivo .env")
        return
    
    print(f"✅ API key configurada: {news_api_key[:10]}...")
    print()
    
    # Categorías a probar
    categories = [
        "general",
        "business", 
        "entertainment",
        "health",
        "science",
        "sports",
        "technology"
    ]
    
    category_names = {
        "general": "Generales",
        "business": "Negocios", 
        "entertainment": "Entretenimiento",
        "health": "Salud",
        "science": "Ciencia", 
        "sports": "Deportes",
        "technology": "Tecnología"
    }
    
    results = {}
    
    for category in categories:
        print(f"🔍 Probando categoría: {category_names[category]} ({category})")
        
        try:
            url = f"https://newsapi.org/v2/top-headlines?country=es&category={category}&apiKey={news_api_key}"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if response.status_code == 200:
                total_results = data.get('totalResults', 0)
                articles_count = len(data.get('articles', []))
                
                if articles_count > 0:
                    results[category] = {
                        "status": "✅",
                        "message": f"{articles_count} noticias encontradas (total: {total_results})",
                        "sample_title": data['articles'][0].get('title', 'Sin título')[:60] + "..."
                    }
                else:
                    results[category] = {
                        "status": "⚠️",
                        "message": "Sin noticias disponibles",
                        "sample_title": "N/A"
                    }
            else:
                error_msg = data.get('message', f'HTTP {response.status_code}')
                results[category] = {
                    "status": "❌",
                    "message": f"Error: {error_msg}",
                    "sample_title": "N/A"
                }
                
        except requests.exceptions.Timeout:
            results[category] = {
                "status": "⏰",
                "message": "Timeout - conexión lenta",
                "sample_title": "N/A"
            }
            
        except requests.exceptions.ConnectionError:
            results[category] = {
                "status": "🌐",
                "message": "Error de conexión",
                "sample_title": "N/A"
            }
            
        except Exception as e:
            results[category] = {
                "status": "💥",
                "message": f"Error: {str(e)}",
                "sample_title": "N/A"
            }
        
        print(f"   {results[category]['status']} {results[category]['message']}")
        if results[category]['sample_title'] != "N/A":
            print(f"   📰 Ejemplo: {results[category]['sample_title']}")
        print()
    
    # Resumen
    print("📊 Resumen de resultados:")
    print("-" * 30)
    
    working = 0
    for category, result in results.items():
        status_emoji = result['status']
        category_name = category_names[category]
        print(f"{status_emoji} {category_name}: {result['message']}")
        if status_emoji == "✅":
            working += 1
    
    print()
    print(f"📈 {working}/{len(categories)} categorías funcionando correctamente")
    
    if working == len(categories):
        print("🎉 ¡Todas las categorías funcionan perfectamente!")
    elif working > 0:
        print("👍 La mayoría de categorías funcionan. Algunos problemas menores.")
    else:
        print("⚠️ Ninguna categoría funciona. Verifica tu API key y conexión.")
    
    # Diagnóstico específico para tecnología
    if 'technology' in results and results['technology']['status'] != "✅":
        print()
        print("🔧 Diagnóstico específico para Tecnología:")
        print(f"   Error: {results['technology']['message']}")
        print("   Posibles causas:")
        print("   - NewsAPI puede no tener noticias de tecnología para España")
        print("   - Intenta cambiar el país a 'us' en la configuración")
        print("   - La categoría 'technology' puede tener restricciones regionales")

def main():
    """Función principal"""
    try:
        test_news_api()
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
    
    print()
    input("Presiona Enter para continuar...")

if __name__ == "__main__":
    main()
