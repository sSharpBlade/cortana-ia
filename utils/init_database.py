#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inicializar Base de Datos para Angie Advanced
===========================================

Este script crea la base de datos SQLite con todas las tablas necesarias.

Autor: Asistente IA
Fecha: 2025
"""

import sqlite3
import os

def initialize_database():
    """Inicializar la base de datos con todas las tablas necesarias"""
    print("🚀 Inicializando base de datos para Angie Advanced...")
    
    try:
        # Conectar a la base de datos (se crea si no existe)
        conn = sqlite3.connect('angie_data.db')
        cursor = conn.cursor()
        
        # Crear tabla de recordatorios
        print("📅 Creando tabla de recordatorios...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                datetime TEXT NOT NULL,
                completed BOOLEAN DEFAULT 0
            )
        ''')
        
        # Crear tabla de tareas
        print("✅ Creando tabla de tareas...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                priority TEXT DEFAULT 'medium',
                completed BOOLEAN DEFAULT 0,
                created_date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Crear tabla de notas
        print("📝 Creando tabla de notas...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_date TEXT DEFAULT CURRENT_TIMESTAMP,
                modified_date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Confirmar cambios
        conn.commit()
        
        # Verificar que las tablas se crearon correctamente
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("\n✅ Base de datos inicializada correctamente!")
        print("📋 Tablas creadas:")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            print(f"   • {table[0]}: {count} registros")
        
        conn.close()
        
        print(f"\n💾 Base de datos guardada como: {os.path.abspath('angie_data.db')}")
        return True
        
    except Exception as e:
        print(f"❌ Error al inicializar la base de datos: {e}")
        return False

def main():
    """Función principal"""
    print("=" * 60)
    print("🗄️  INICIALIZACIÓN DE BASE DE DATOS - ANGIE ADVANCED")
    print("=" * 60)
    
    if initialize_database():
        print("\n✅ La base de datos está lista para usar!")
        print("\n🚀 Ahora puedes:")
        print("   1. Ejecutar Angie Advanced: python angie_advanced.py")
        print("   2. Probar el sistema de notas: python test_notes_system.py")
    else:
        print("\n❌ Error al inicializar la base de datos")
        print("Revisa los permisos del directorio y vuelve a intentar")

if __name__ == "__main__":
    main()
