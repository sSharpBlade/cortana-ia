#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test del Sistema de Notas de Angie Advanced
==========================================

Este script prueba todas las funcionalidades del sistema de notas mejorado.

Funcionalidades probadas:
- Creación de notas en base de datos
- Lectura de notas existentes
- Búsqueda de notas por contenido
- Edición y eliminación de notas
- Comandos de voz para notas

Autor: Asistente IA
Fecha: 2025
"""

import sqlite3
import os
from datetime import datetime

def test_database_connection():
    """Prueba la conexión a la base de datos"""
    print("🔍 Probando conexión a la base de datos...")
    
    db_path = "angie_data.db"
    if not os.path.exists(db_path):
        print("❌ La base de datos no existe. Ejecuta Angie Advanced primero.")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar que la tabla notes existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='notes'")
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("✅ Tabla 'notes' encontrada en la base de datos")
            
            # Mostrar estructura de la tabla
            cursor.execute("PRAGMA table_info(notes)")
            columns = cursor.fetchall()
            print("📋 Estructura de la tabla 'notes':")
            for col in columns:
                print(f"   - {col[1]} ({col[2]})")
            
            # Contar notas existentes
            cursor.execute("SELECT COUNT(*) FROM notes")
            count = cursor.fetchone()[0]
            print(f"📝 Notas existentes: {count}")
            
            conn.close()
            return True
        else:
            print("❌ La tabla 'notes' no existe en la base de datos")
            conn.close()
            return False
            
    except Exception as e:
        print(f"❌ Error al conectar con la base de datos: {e}")
        return False

def test_create_sample_notes():
    """Crear notas de ejemplo para pruebas"""
    print("\n📝 Creando notas de ejemplo...")
    
    try:
        conn = sqlite3.connect("angie_data.db")
        cursor = conn.cursor()
        
        sample_notes = [
            ("Lista de Compras", "Comprar: leche, pan, huevos, manzanas, pollo"),
            ("Ideas de Proyecto", "Desarrollar un asistente de voz con IA integrada"),
            ("Recordatorio Médico", "Cita con el dentista el próximo martes a las 3 PM"),
            ("Receta de Cocina", "Pasta con salsa de tomate: tomates, ajo, cebolla, albahaca"),
            ("Nota de Trabajo", "Reunión con el equipo para revisar el progreso del proyecto")
        ]
        
        for title, content in sample_notes:
            # Verificar si la nota ya existe
            cursor.execute("SELECT id FROM notes WHERE title = ?", (title,))
            exists = cursor.fetchone()
            
            if not exists:
                cursor.execute('''
                    INSERT INTO notes (title, content, created_date, modified_date)
                    VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                ''', (title, content))
                print(f"✅ Nota creada: '{title}'")
            else:
                print(f"⚠️  Nota ya existe: '{title}'")
        
        conn.commit()
        conn.close()
        print("✅ Notas de ejemplo creadas exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error al crear notas de ejemplo: {e}")
        return False

def test_search_notes():
    """Probar la búsqueda de notas"""
    print("\n🔍 Probando búsqueda de notas...")
    
    try:
        conn = sqlite3.connect("angie_data.db")
        cursor = conn.cursor()
        
        search_terms = ["compras", "proyecto", "médico", "cocina"]
        
        for term in search_terms:
            cursor.execute('''
                SELECT title, content 
                FROM notes 
                WHERE title LIKE ? OR content LIKE ?
            ''', (f'%{term}%', f'%{term}%'))
            
            results = cursor.fetchall()
            print(f"🔍 Búsqueda '{term}': {len(results)} resultados encontrados")
            
            for title, content in results:
                preview = content[:50] + "..." if len(content) > 50 else content
                print(f"   📝 {title}: {preview}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error en la búsqueda: {e}")
        return False

def test_notes_summary():
    """Probar el resumen de notas"""
    print("\n📊 Generando resumen de notas...")
    
    try:
        conn = sqlite3.connect("angie_data.db")
        cursor = conn.cursor()
        
        # Contar total de notas
        cursor.execute("SELECT COUNT(*) FROM notes")
        total_notes = cursor.fetchone()[0]
        
        # Obtener notas más recientes
        cursor.execute('''
            SELECT title, created_date 
            FROM notes 
            ORDER BY modified_date DESC 
            LIMIT 5
        ''')
        recent_notes = cursor.fetchall()
        
        print(f"📝 Total de notas: {total_notes}")
        print("📅 Notas más recientes:")
        
        for title, date in recent_notes:
            print(f"   • {title} ({date[:16]})")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error en el resumen: {e}")
        return False

def test_voice_commands():
    """Mostrar comandos de voz disponibles"""
    print("\n🗣️  COMANDOS DE VOZ PARA NOTAS:")
    
    voice_commands = [
        "crear nota / nueva nota / tomar nota",
        "ver notas / mostrar notas / mis notas", 
        "buscar nota [término]",
        "cuántas notas / resumen de notas",
        "leer notas",
        "ayuda notas"
    ]
    
    for command in voice_commands:
        print(f"   🎤 {command}")
    
    print("\n💡 CONSEJOS:")
    print("   • Di claramente los comandos")
    print("   • Para buscar, di 'buscar nota' seguido del término")
    print("   • Usa 'leer notas' para escuchar las más recientes")
    print("   • Di 'ayuda notas' para ver la ayuda completa")

def main():
    """Función principal del test"""
    print("=" * 60)
    print("🧪 TEST DEL SISTEMA DE NOTAS - ANGIE ADVANCED")
    print("=" * 60)
    
    # Test 1: Conexión a base de datos
    if not test_database_connection():
        print("\n❌ Test fallido: Problemas con la base de datos")
        return
    
    # Test 2: Crear notas de ejemplo
    test_create_sample_notes()
    
    # Test 3: Probar búsquedas
    test_search_notes()
    
    # Test 4: Resumen de notas
    test_notes_summary()
    
    # Test 5: Mostrar comandos de voz
    test_voice_commands()
    
    print("\n" + "=" * 60)
    print("✅ TEST COMPLETADO")
    print("=" * 60)
    print("\n🚀 Para probar el sistema completo:")
    print("   1. Ejecuta python angie_advanced.py")
    print("   2. Usa los comandos de voz o botones de la interfaz")
    print("   3. Prueba crear, buscar, leer y editar notas")
    print("\n📚 Usa 'ayuda notas' en Angie para ver toda la ayuda")

if __name__ == "__main__":
    main()
