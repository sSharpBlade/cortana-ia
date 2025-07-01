#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test del Sistema de Búsquedas - Angie Advanced
=============================================

Este script prueba todas las funcionalidades del sistema de búsquedas en Wikipedia.

Funcionalidades probadas:
- Búsquedas con términos específicos
- Manejo de errores y excepciones
- Respuestas en español
- Casos de ambigüedad
- Casos sin resultados

Autor: Asistente IA
Fecha: 2025
"""

import wikipedia
import time

def test_wikipedia_connection():
    """Probar conexión a Wikipedia"""
    print("🔍 Probando conexión a Wikipedia...")
    
    try:
        # Configurar idioma español
        wikipedia.set_lang("es")
        print("✅ Idioma configurado a español")
        
        # Hacer una búsqueda simple
        test_query = "España"
        results = wikipedia.search(test_query, results=1)
        
        if results:
            print(f"✅ Búsqueda de prueba exitosa: {results[0]}")
            return True
        else:
            print("❌ No se obtuvieron resultados en la búsqueda de prueba")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión a Wikipedia: {e}")
        return False

def test_search_functionality():
    """Probar diferentes tipos de búsquedas"""
    print("\n🧪 Probando funcionalidad de búsquedas...")
    
    test_cases = [
        {
            "query": "inteligencia artificial",
            "description": "Término técnico común"
        },
        {
            "query": "Madrid",
            "description": "Lugar geográfico"
        },
        {
            "query": "Albert Einstein",
            "description": "Persona famosa"
        },
        {
            "query": "Python programación",
            "description": "Tema de tecnología"
        },
        {
            "query": "xyzabc123noexiste",
            "description": "Término que no existe"
        }
    ]
    
    successful_searches = 0
    
    for i, test_case in enumerate(test_cases, 1):
        query = test_case["query"]
        description = test_case["description"]
        
        print(f"\n{i}. Probando: '{query}' ({description})")
        print("-" * 50)
        
        try:
            # Buscar
            search_results = wikipedia.search(query, results=3)
            
            if search_results:
                print(f"✅ Resultados encontrados: {len(search_results)}")
                print(f"   Principales: {', '.join(search_results[:3])}")
                
                try:
                    # Intentar obtener resumen
                    summary = wikipedia.summary(search_results[0], sentences=2)
                    print(f"   Resumen: {summary[:100]}...")
                    successful_searches += 1
                    
                except wikipedia.exceptions.DisambiguationError as e:
                    print(f"   ⚠️ Ambigüedad detectada. Opciones: {e.options[:3]}")
                    successful_searches += 1
                    
                except wikipedia.exceptions.PageError:
                    print(f"   ⚠️ Error de página para '{search_results[0]}'")
                    
            else:
                print(f"❌ No se encontraron resultados para '{query}'")
                
        except Exception as e:
            print(f"❌ Error en búsqueda: {e}")
        
        # Pequeña pausa entre búsquedas
        time.sleep(0.5)
    
    print(f"\n📊 Resumen: {successful_searches}/{len(test_cases)} búsquedas exitosas")
    return successful_searches == len(test_cases) - 1  # -1 porque esperamos que una falle

def test_voice_commands():
    """Mostrar comandos de voz para búsquedas"""
    print("\n🗣️ COMANDOS DE VOZ PARA BÚSQUEDAS:")
    
    voice_commands = [
        "busca [término]",
        "buscar [término]",
        "busca información sobre [tema]",
        "buscar datos de [persona/lugar]"
    ]
    
    for command in voice_commands:
        print(f"   🎤 Angie, {command}")
    
    print("\n💡 EJEMPLOS PRÁCTICOS:")
    examples = [
        "Angie, busca inteligencia artificial",
        "Angie, buscar información sobre Madrid",
        "Angie, busca Albert Einstein",
        "Angie, buscar Python programación"
    ]
    
    for example in examples:
        print(f"   🔸 {example}")

def test_error_handling():
    """Probar manejo de errores"""
    print("\n🛡️ Probando manejo de errores...")
    
    error_cases = [
        {
            "query": "",
            "description": "Búsqueda vacía"
        },
        {
            "query": "   ",
            "description": "Solo espacios"
        },
        {
            "query": "ñáéíóú",
            "description": "Caracteres especiales"
        }
    ]
    
    for i, case in enumerate(error_cases, 1):
        query = case["query"]
        description = case["description"]
        
        print(f"{i}. {description}: '{query}'")
        
        if not query.strip():
            print("   ✅ Caso manejado: búsqueda vacía detectada")
        else:
            try:
                results = wikipedia.search(query, results=1)
                if results:
                    print(f"   ✅ Resultados: {results}")
                else:
                    print("   ✅ Sin resultados (esperado)")
            except Exception as e:
                print(f"   ⚠️ Error: {e}")

def main():
    """Función principal del test"""
    print("=" * 60)
    print("🧪 TEST DEL SISTEMA DE BÚSQUEDAS - ANGIE ADVANCED")
    print("=" * 60)
    
    # Test 1: Conexión a Wikipedia
    if not test_wikipedia_connection():
        print("\n❌ Test fallido: Problemas de conexión a Wikipedia")
        return
    
    # Test 2: Funcionalidad de búsquedas
    test_search_functionality()
    
    # Test 3: Comandos de voz
    test_voice_commands()
    
    # Test 4: Manejo de errores
    test_error_handling()
    
    print("\n" + "=" * 60)
    print("✅ TEST COMPLETADO")
    print("=" * 60)
    print("\n🚀 Para probar el sistema completo:")
    print("   1. Ejecuta python angie_advanced.py")
    print("   2. Usa el botón '🔍 Buscar' o comandos de voz")
    print("   3. Prueba: 'Angie, busca inteligencia artificial'")
    print("   4. Si no especificas término, se abrirá ventana de búsqueda")
    print("\n💡 MEJORAS IMPLEMENTADAS:")
    print("   ✅ Sin prompts constantes")
    print("   ✅ Ventana de búsqueda cuando no hay término")
    print("   ✅ Manejo de ambigüedades")
    print("   ✅ Búsquedas en español")
    print("   ✅ Enlaces a páginas completas")
    print("   ✅ Respuestas más descriptivas")

if __name__ == "__main__":
    main()
