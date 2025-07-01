#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo Interactivo del Sistema de Notas - Angie Advanced
====================================================

Este script demuestra todas las funcionalidades del sistema de notas mejorado
de forma interactiva.

Autor: Asistente IA
Fecha: 2025
"""

import sqlite3
import os
from datetime import datetime

class NotesDemo:
    def __init__(self):
        self.conn = sqlite3.connect('angie_data.db')
        self.cursor = self.conn.cursor()
        
    def display_menu(self):
        """Mostrar menú principal"""
        print("\n" + "=" * 60)
        print("📝 DEMO DEL SISTEMA DE NOTAS - ANGIE ADVANCED")
        print("=" * 60)
        print("¿Qué quieres hacer?")
        print()
        print("1. 📝 Crear una nueva nota")
        print("2. 📚 Ver todas las notas")
        print("3. 🔍 Buscar notas")
        print("4. 📊 Ver resumen de notas")
        print("5. 🗣️  Simular comando de voz")
        print("6. ❌ Eliminar una nota")
        print("7. ✏️  Editar una nota")
        print("8. 🧪 Ejecutar tests automáticos")
        print("9. ❓ Ver ayuda de comandos")
        print("0. 🚪 Salir")
        print()
        
    def create_note(self):
        """Crear una nueva nota"""
        print("\n📝 CREAR NUEVA NOTA")
        print("-" * 30)
        
        title = input("Título de la nota: ").strip()
        if not title:
            title = f"Nota {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
        print("Contenido de la nota (termina con línea vacía):")
        content_lines = []
        while True:
            line = input()
            if line.strip() == "":
                break
            content_lines.append(line)
        
        content = "\n".join(content_lines)
        
        if content.strip():
            try:
                self.cursor.execute('''
                    INSERT INTO notes (title, content, created_date, modified_date)
                    VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                ''', (title, content))
                self.conn.commit()
                print(f"✅ Nota '{title}' guardada exitosamente!")
            except Exception as e:
                print(f"❌ Error al guardar la nota: {e}")
        else:
            print("⚠️ Nota cancelada - contenido vacío")
    
    def view_all_notes(self):
        """Ver todas las notas"""
        print("\n📚 TODAS LAS NOTAS")
        print("-" * 30)
        
        self.cursor.execute('''
            SELECT id, title, content, created_date, modified_date 
            FROM notes 
            ORDER BY modified_date DESC
        ''')
        notes = self.cursor.fetchall()
        
        if not notes:
            print("📭 No hay notas guardadas")
            return
            
        for i, (note_id, title, content, created, modified) in enumerate(notes, 1):
            print(f"\n{i}. 📝 {title}")
            print(f"   ID: {note_id}")
            print(f"   Creada: {created[:16]}")
            print(f"   Modificada: {modified[:16]}")
            
            # Mostrar preview del contenido
            preview = content[:100] + "..." if len(content) > 100 else content
            print(f"   Contenido: {preview}")
            print("   " + "-" * 50)
    
    def search_notes(self):
        """Buscar notas"""
        print("\n🔍 BUSCAR NOTAS")
        print("-" * 30)
        
        search_term = input("Término de búsqueda: ").strip()
        
        if not search_term:
            print("⚠️ Término de búsqueda vacío")
            return
            
        self.cursor.execute('''
            SELECT id, title, content, created_date 
            FROM notes 
            WHERE title LIKE ? OR content LIKE ?
            ORDER BY modified_date DESC
        ''', (f'%{search_term}%', f'%{search_term}%'))
        
        results = self.cursor.fetchall()
        
        if not results:
            print(f"❌ No se encontraron notas con '{search_term}'")
            return
            
        print(f"✅ Se encontraron {len(results)} notas:")
        
        for note_id, title, content, created in results:
            print(f"\n📝 {title}")
            print(f"   ID: {note_id} | Creada: {created[:16]}")
            
            # Resaltar el término encontrado
            preview = content[:150] + "..." if len(content) > 150 else content
            highlighted = preview.replace(search_term, f"**{search_term}**")
            print(f"   {highlighted}")
    
    def notes_summary(self):
        """Mostrar resumen de notas"""
        print("\n📊 RESUMEN DE NOTAS")
        print("-" * 30)
        
        # Contar total
        self.cursor.execute("SELECT COUNT(*) FROM notes")
        total = self.cursor.fetchone()[0]
        
        print(f"📝 Total de notas: {total}")
        
        if total == 0:
            return
            
        # Notas más recientes
        self.cursor.execute('''
            SELECT title, created_date 
            FROM notes 
            ORDER BY modified_date DESC 
            LIMIT 3
        ''')
        recent = self.cursor.fetchall()
        
        print("\n📅 Notas más recientes:")
        for title, date in recent:
            print(f"   • {title} ({date[:16]})")
        
        # Estadísticas por fecha
        self.cursor.execute('''
            SELECT DATE(created_date) as date, COUNT(*) as count
            FROM notes 
            GROUP BY DATE(created_date)
            ORDER BY date DESC
            LIMIT 5
        ''')
        daily_stats = self.cursor.fetchall()
        
        if daily_stats:
            print("\n📈 Notas por día:")
            for date, count in daily_stats:
                print(f"   • {date}: {count} nota{'s' if count != 1 else ''}")
    
    def simulate_voice_command(self):
        """Simular comandos de voz"""
        print("\n🗣️ SIMULAR COMANDO DE VOZ")
        print("-" * 30)
        print("Comandos disponibles:")
        print("• crear nota")
        print("• ver notas") 
        print("• buscar nota [término]")
        print("• cuántas notas")
        print("• leer notas")
        print()
        
        command = input("Comando de voz: ").strip().lower()
        
        if "crear nota" in command:
            print("🎤 Comando detectado: CREAR NOTA")
            self.create_note()
            
        elif "ver notas" in command:
            print("🎤 Comando detectado: VER NOTAS")
            self.view_all_notes()
            
        elif "buscar nota" in command:
            print("🎤 Comando detectado: BUSCAR NOTA")
            search_term = command.replace("buscar nota", "").strip()
            if search_term:
                print(f"🔍 Buscando: {search_term}")
                self.cursor.execute('''
                    SELECT title, content FROM notes 
                    WHERE title LIKE ? OR content LIKE ?
                ''', (f'%{search_term}%', f'%{search_term}%'))
                results = self.cursor.fetchall()
                
                if results:
                    print(f"✅ {len(results)} resultado(s) encontrado(s)")
                    for title, content in results[:3]:
                        print(f"📝 {title}: {content[:50]}...")
                else:
                    print("❌ No se encontraron resultados")
            else:
                self.search_notes()
                
        elif "cuántas notas" in command:
            print("🎤 Comando detectado: CUÁNTAS NOTAS")
            self.notes_summary()
            
        elif "leer notas" in command:
            print("🎤 Comando detectado: LEER NOTAS")
            self.cursor.execute('''
                SELECT title, content FROM notes 
                ORDER BY modified_date DESC LIMIT 3
            ''')
            notes = self.cursor.fetchall()
            
            if notes:
                print("🔊 Leyendo notas recientes:")
                for i, (title, content) in enumerate(notes, 1):
                    print(f"Nota {i}: {title}. {content}")
            else:
                print("📭 No hay notas para leer")
        else:
            print("❓ Comando no reconocido")
    
    def delete_note(self):
        """Eliminar una nota"""
        print("\n❌ ELIMINAR NOTA")
        print("-" * 30)
        
        self.view_all_notes()
        
        try:
            note_id = int(input("\nID de la nota a eliminar: "))
            
            # Verificar que la nota existe
            self.cursor.execute("SELECT title FROM notes WHERE id = ?", (note_id,))
            note = self.cursor.fetchone()
            
            if not note:
                print("❌ Nota no encontrada")
                return
                
            confirm = input(f"¿Eliminar la nota '{note[0]}'? (s/n): ").lower()
            
            if confirm == 's':
                self.cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
                self.conn.commit()
                print("✅ Nota eliminada exitosamente")
            else:
                print("❌ Eliminación cancelada")
                
        except ValueError:
            print("❌ ID inválido")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def edit_note(self):
        """Editar una nota"""
        print("\n✏️ EDITAR NOTA")
        print("-" * 30)
        
        self.view_all_notes()
        
        try:
            note_id = int(input("\nID de la nota a editar: "))
            
            # Obtener nota actual
            self.cursor.execute("SELECT title, content FROM notes WHERE id = ?", (note_id,))
            note = self.cursor.fetchone()
            
            if not note:
                print("❌ Nota no encontrada")
                return
            
            current_title, current_content = note
            
            print(f"\nTítulo actual: {current_title}")
            new_title = input("Nuevo título (Enter para mantener): ").strip()
            if not new_title:
                new_title = current_title
            
            print(f"\nContenido actual:\n{current_content}")
            print("\nNuevo contenido (termina con línea vacía):")
            
            content_lines = []
            while True:
                line = input()
                if line.strip() == "":
                    break
                content_lines.append(line)
            
            if content_lines:
                new_content = "\n".join(content_lines)
            else:
                new_content = current_content
            
            # Actualizar nota
            self.cursor.execute('''
                UPDATE notes 
                SET title = ?, content = ?, modified_date = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (new_title, new_content, note_id))
            self.conn.commit()
            
            print("✅ Nota actualizada exitosamente")
            
        except ValueError:
            print("❌ ID inválido")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def run_tests(self):
        """Ejecutar tests automáticos"""
        print("\n🧪 EJECUTANDO TESTS AUTOMÁTICOS")
        print("-" * 40)
        
        os.system("python test_notes_system.py")
    
    def show_help(self):
        """Mostrar ayuda de comandos"""
        print("\n❓ AYUDA DE COMANDOS")
        print("-" * 30)
        print("🗣️ COMANDOS DE VOZ:")
        print("• 'crear nota' - Crear nueva nota")
        print("• 'ver notas' - Ver todas las notas")  
        print("• 'buscar nota [término]' - Buscar notas")
        print("• 'cuántas notas' - Resumen de notas")
        print("• 'leer notas' - Leer notas recientes")
        print("• 'ayuda notas' - Mostrar ayuda")
        print()
        print("🖱️ INTERFAZ GRÁFICA:")
        print("• Botón '📝 Nueva Nota'")
        print("• Botón '📚 Ver Notas'") 
        print("• En cada nota: Leer, Editar, Eliminar, Copiar")
        print()
        print("💬 COMANDOS DE TEXTO:")
        print("• Escribe los comandos de voz en el chat")
        print("• Ejemplo: 'buscar nota compras'")
    
    def run(self):
        """Ejecutar el demo interactivo"""
        print("🚀 Bienvenido al Demo del Sistema de Notas de Angie Advanced!")
        
        while True:
            self.display_menu()
            
            try:
                choice = input("Selecciona una opción (0-9): ").strip()
                
                if choice == "1":
                    self.create_note()
                elif choice == "2":
                    self.view_all_notes()
                elif choice == "3":
                    self.search_notes()
                elif choice == "4":
                    self.notes_summary()
                elif choice == "5":
                    self.simulate_voice_command()
                elif choice == "6":
                    self.delete_note()
                elif choice == "7":
                    self.edit_note()
                elif choice == "8":
                    self.run_tests()
                elif choice == "9":
                    self.show_help()
                elif choice == "0":
                    print("\n👋 ¡Gracias por probar el sistema de notas!")
                    print("🚀 Ahora puedes usar Angie Advanced con todas estas funcionalidades")
                    break
                else:
                    print("❌ Opción inválida. Intenta de nuevo.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Demo terminado. ¡Hasta luego!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
        
        self.conn.close()

def main():
    """Función principal"""
    # Verificar que la base de datos existe
    if not os.path.exists('angie_data.db'):
        print("❌ Base de datos no encontrada.")
        print("🔧 Ejecuta primero: python init_database.py")
        return
    
    try:
        demo = NotesDemo()
        demo.run()
    except Exception as e:
        print(f"❌ Error al ejecutar el demo: {e}")

if __name__ == "__main__":
    main()
