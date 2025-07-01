#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demostración rápida de comandos de clima para el asistente Angie
"""

from angie_advanced_temp import AngieAdvancedTemp
import time

def demo_clima():
    """Demuestra los comandos de clima disponibles"""
    print("🤖 Demo de Comandos de Clima - Asistente Angie")
    print("=" * 55)
    print("🏙️ Ciudad configurada: Ambato, Ecuador")
    print("🌤️ API: WeatherAPI.com")
    print()
    
    # Crear instancia del asistente
    angie = AngieAdvancedTemp()
    
    # Lista de comandos para probar
    comandos_clima = [
        "clima",
        "tiempo",
        "qué clima hay",
        "clima en Quito",
        "tiempo de Guayaquil", 
        "cómo está el clima en Cuenca",
        "clima de Loja"
    ]
    
    print("🧪 Probando comandos de clima:")
    print("-" * 40)
    
    for i, comando in enumerate(comandos_clima, 1):
        print(f"\n{i}. Comando: '{comando}'")
        print("   Respuesta:")
        
        try:
            # Simular el procesamiento del comando
            angie.process_command(comando)
            time.sleep(1)  # Pausa para ver el resultado
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n🎉 Demo completada!")
    print("\n💡 Consejos:")
    print("   • Usa el asistente con interfaz gráfica para mejor experiencia")
    print("   • Puedes cambiar la ciudad por defecto en el archivo .env")
    print("   • Prueba comandos de voz si tienes micrófono configurado")

if __name__ == "__main__":
    demo_clima()
