#!/usr/bin/env python3
"""
Script para visualizar el entrenamiento LSTM con diagramas interactivos en Python
Genera y muestra gráficos del entrenamiento del modelo
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os
import random

# Configurar matplotlib para mejor visualización
plt.style.use('default')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3

class LSTMTrainingVisualizer:
    def __init__(self):
        """Inicializar visualizador de entrenamiento LSTM"""
        self.colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
        self.setup_style()
        
    def setup_style(self):
        """Configurar estilo de gráficos"""
        sns.set_palette("husl")
        plt.rcParams['font.family'] = 'DejaVu Sans'
        
    def generate_training_data(self, epochs=20):
        """Generar datos simulados de entrenamiento"""
        # Datos de entrenamiento simulados
        train_loss = 2.5 * np.exp(-np.arange(epochs)/5) + 0.1 + np.random.normal(0, 0.05, epochs)
        val_loss = 2.3 * np.exp(-np.arange(epochs)/4.5) + 0.15 + np.random.normal(0, 0.08, epochs)
        train_acc = 1 - 0.8 * np.exp(-np.arange(epochs)/4) + np.random.normal(0, 0.02, epochs)
        val_acc = 1 - 0.85 * np.exp(-np.arange(epochs)/3.5) + np.random.normal(0, 0.03, epochs)
        
        return {
            'epochs': np.arange(1, epochs + 1),
            'train_loss': train_loss,
            'val_loss': val_loss,
            'train_acc': train_acc,
            'val_acc': val_acc
        }
    
    def plot_training_curves(self, data):
        """Gráfico de curvas de entrenamiento"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Gráfico de pérdida
        ax1.plot(data['epochs'], data['train_loss'], 'b-', label='Pérdida de Entrenamiento', 
                linewidth=2, marker='o', markersize=6)
        ax1.plot(data['epochs'], data['val_loss'], 'r-', label='Pérdida de Validación', 
                linewidth=2, marker='s', markersize=6)
        ax1.set_title('Evolución de la Pérdida', fontsize=16, fontweight='bold')
        ax1.set_xlabel('Época', fontsize=12)
        ax1.set_ylabel('Pérdida', fontsize=12)
        ax1.legend(fontsize=11)
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(0, max(data['train_loss']) * 1.1)
        
        # Gráfico de precisión
        ax2.plot(data['epochs'], data['train_acc'], 'b-', label='Precisión de Entrenamiento', 
                linewidth=2, marker='o', markersize=6)
        ax2.plot(data['epochs'], data['val_acc'], 'r-', label='Precisión de Validación', 
                linewidth=2, marker='s', markersize=6)
        ax2.set_title('Evolución de la Precisión', fontsize=16, fontweight='bold')
        ax2.set_xlabel('Época', fontsize=12)
        ax2.set_ylabel('Precisión', fontsize=12)
        ax2.legend(fontsize=11)
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(0, 1.05)
        
        plt.tight_layout()
        plt.show()
        
        return fig
    
    def plot_confusion_matrix(self):
        """Gráfico de matriz de confusión"""
        # Datos simulados de matriz de confusión
        command_types = ['time', 'weather', 'search', 'music', 'notes', 'screenshot', 'system', 'chat']
        confusion_matrix = np.array([
            [15, 1, 0, 0, 0, 0, 0, 1],
            [1, 12, 1, 0, 0, 0, 0, 0],
            [0, 1, 18, 1, 0, 0, 0, 0],
            [0, 0, 1, 14, 1, 0, 0, 0],
            [0, 0, 0, 1, 10, 0, 0, 0],
            [0, 0, 0, 0, 0, 8, 0, 0],
            [0, 0, 0, 0, 0, 0, 6, 0],
            [1, 0, 0, 0, 0, 0, 0, 20]
        ])
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(confusion_matrix, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=command_types, yticklabels=command_types)
        plt.title('Matriz de Confusión - Modelo LSTM', fontsize=16, fontweight='bold')
        plt.xlabel('Predicción', fontsize=12)
        plt.ylabel('Valor Real', fontsize=12)
        plt.xticks(rotation=45)
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.show()
        
        return plt.gcf()
    
    def plot_command_distribution(self):
        """Gráfico de distribución de comandos"""
        command_types = ['time', 'weather', 'search', 'music', 'notes', 'screenshot', 'system', 'reminder', 'news', 'navigation', 'tasks', 'chat']
        command_counts = [156, 134, 189, 145, 98, 67, 89, 112, 123, 78, 95, 141]
        
        plt.figure(figsize=(14, 8))
        bars = plt.bar(range(len(command_types)), command_counts, color=self.colors[:len(command_types)])
        plt.title('Distribución de Tipos de Comandos', fontsize=16, fontweight='bold')
        plt.xlabel('Tipo de Comando', fontsize=12)
        plt.ylabel('Frecuencia', fontsize=12)
        plt.xticks(range(len(command_types)), command_types, rotation=45)
        
        # Agregar valores en las barras
        for bar, count in zip(bars, command_counts):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                    str(count), ha='center', va='bottom', fontweight='bold', fontsize=11)
        
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.show()
        
        return plt.gcf()
    
    def plot_command_length_analysis(self):
        """Análisis de longitud de comandos"""
        # Datos simulados
        command_types = ['time', 'weather', 'search', 'music', 'notes', 'screenshot', 'system', 'chat']
        avg_lengths = [12, 15, 18, 14, 16, 20, 19, 25]
        std_lengths = [3, 4, 5, 3, 4, 6, 5, 7]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Histograma de longitudes
        all_lengths = []
        for i, cmd_type in enumerate(command_types):
            lengths = np.random.normal(avg_lengths[i], std_lengths[i], 50)
            all_lengths.extend(lengths)
        
        ax1.hist(all_lengths, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        ax1.set_title('Distribución de Longitud de Comandos', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Longitud del Comando')
        ax1.set_ylabel('Frecuencia')
        ax1.grid(True, alpha=0.3)
        
        # Gráfico de barras por tipo
        bars = ax2.bar(command_types, avg_lengths, yerr=std_lengths, capsize=5, 
                      color=self.colors[:len(command_types)], alpha=0.8)
        ax2.set_title('Longitud Promedio por Tipo de Comando', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Tipo de Comando')
        ax2.set_ylabel('Longitud Promedio')
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.show()
        
        return fig
    
    def plot_word_frequency(self):
        """Gráfico de frecuencia de palabras"""
        # Datos simulados de palabras más frecuentes
        words = ['qué', 'hora', 'clima', 'busca', 'reproduce', 'música', 'nota', 'captura', 'sistema', 'recordatorio', 'noticias', 'abre', 'tarea', 'hola']
        frequencies = [45, 38, 32, 28, 25, 22, 18, 15, 12, 10, 8, 6, 5, 4]
        
        plt.figure(figsize=(12, 8))
        bars = plt.barh(range(len(words)), frequencies, color='lightcoral')
        plt.title('Palabras Más Frecuentes en Comandos', fontsize=16, fontweight='bold')
        plt.xlabel('Frecuencia', fontsize=12)
        plt.ylabel('Palabras', fontsize=12)
        plt.yticks(range(len(words)), words)
        
        # Agregar valores en las barras
        for i, (bar, freq) in enumerate(zip(bars, frequencies)):
            plt.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                    str(freq), ha='left', va='center', fontweight='bold', fontsize=11)
        
        plt.grid(True, alpha=0.3, axis='x')
        plt.tight_layout()
        plt.show()
        
        return plt.gcf()
    
    def plot_metrics_summary(self, data):
        """Resumen completo de métricas"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Métricas principales
        metrics_data = {
            'Precisión': [94.2],
            'Total Comandos': [1247],
            'Tipos Únicos': [12],
            'Palabras Únicas': [247]
        }
        
        metrics_df = list(metrics_data.values())
        metrics_names = list(metrics_data.keys())
        
        bars = ax1.bar(metrics_names, [m[0] for m in metrics_df], color=self.colors[:4])
        ax1.set_title('Métricas Principales', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Valor')
        ax1.tick_params(axis='x', rotation=45)
        
        # Agregar valores en las barras
        for bar, value in zip(bars, [m[0] for m in metrics_df]):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max([m[0] for m in metrics_df]) * 0.01,
                    f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
        
        # Precisión por época
        ax2.plot(data['epochs'], data['train_acc'], 'b-', label='Entrenamiento', linewidth=2)
        ax2.plot(data['epochs'], data['val_acc'], 'r-', label='Validación', linewidth=2)
        ax2.set_title('Precisión por Época', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Época')
        ax2.set_ylabel('Precisión')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Pérdida por época
        ax3.plot(data['epochs'], data['train_loss'], 'b-', label='Entrenamiento', linewidth=2)
        ax3.plot(data['epochs'], data['val_loss'], 'r-', label='Validación', linewidth=2)
        ax3.set_title('Pérdida por Época', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Época')
        ax3.set_ylabel('Pérdida')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Actividad por hora (simulada)
        hours = np.arange(24)
        activity = np.random.poisson(5, 24) + np.sin(hours * np.pi / 12) * 3
        ax4.plot(hours, activity, marker='o', linewidth=2, markersize=8, color='green')
        ax4.set_title('Actividad por Hora del Día', fontsize=14, fontweight='bold')
        ax4.set_xlabel('Hora')
        ax4.set_ylabel('Número de Comandos')
        ax4.grid(True, alpha=0.3)
        ax4.set_xticks(range(0, 24, 3))
        
        plt.tight_layout()
        plt.show()
        
        return fig
    
    def plot_model_architecture(self):
        """Visualización de la arquitectura del modelo"""
        fig, ax = plt.subplots(1, 1, figsize=(12, 10))
        
        # Configurar el gráfico
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Título
        ax.text(5, 9.5, 'Arquitectura del Modelo LSTM', fontsize=16, fontweight='bold', 
               ha='center', va='center')
        
        # Capas del modelo
        layers = [
            {'name': 'Input (Texto)', 'y': 8.5, 'color': '#FF6B6B'},
            {'name': 'Embedding (128)', 'y': 7.5, 'color': '#4ECDC4'},
            {'name': 'LSTM Capa 1 (128)', 'y': 6.5, 'color': '#45B7D1'},
            {'name': 'LSTM Capa 2 (64)', 'y': 5.5, 'color': '#96CEB4'},
            {'name': 'LSTM Capa 3 (32)', 'y': 4.5, 'color': '#FFEAA7'},
            {'name': 'Dense (64)', 'y': 3.5, 'color': '#DDA0DD'},
            {'name': 'Dropout (0.3)', 'y': 2.5, 'color': '#FFB6C1'},
            {'name': 'Output (12 clases)', 'y': 1.5, 'color': '#98FB98'}
        ]
        
        # Dibujar capas
        for i, layer in enumerate(layers):
            # Rectángulo de la capa
            rect = plt.Rectangle((2, layer['y']-0.3), 6, 0.6, 
                               facecolor=layer['color'], alpha=0.8, edgecolor='black')
            ax.add_patch(rect)
            
            # Texto de la capa
            ax.text(5, layer['y'], layer['name'], fontsize=11, fontweight='bold',
                   ha='center', va='center')
            
            # Flecha hacia abajo (excepto para la última capa)
            if i < len(layers) - 1:
                ax.arrow(5, layer['y']-0.4, 0, -0.6, head_width=0.1, head_length=0.1, 
                        fc='black', ec='black')
        
        # Información adicional
        ax.text(5, 0.5, 'Modelo LSTM para Clasificación de Comandos\n12 tipos de comandos soportados', 
               fontsize=10, ha='center', va='center', style='italic')
        
        plt.tight_layout()
        plt.show()
        
        return fig
    
    def show_all_visualizations(self):
        """Mostrar todas las visualizaciones"""
        print("🧠 Generando visualizaciones del entrenamiento LSTM...")
        print("=" * 60)
        
        # Generar datos de entrenamiento
        training_data = self.generate_training_data()
        
        # Mostrar cada visualización
        print("📈 1. Curvas de entrenamiento...")
        self.plot_training_curves(training_data)
        
        print("🔍 2. Matriz de confusión...")
        self.plot_confusion_matrix()
        
        print("📊 3. Distribución de comandos...")
        self.plot_command_distribution()
        
        print("📏 4. Análisis de longitud...")
        self.plot_command_length_analysis()
        
        print("📝 5. Frecuencia de palabras...")
        self.plot_word_frequency()
        
        print("📋 6. Resumen de métricas...")
        self.plot_metrics_summary(training_data)
        
        print("🏗️ 7. Arquitectura del modelo...")
        self.plot_model_architecture()
        
        print("\n🎉 ¡Todas las visualizaciones mostradas!")
        print("💡 Cierra cada ventana para continuar con la siguiente")

def main():
    """Función principal"""
    print("🧠 VISUALIZADOR DE ENTRENAMIENTO LSTM")
    print("=" * 50)
    print("📊 Mostrando diagramas de entrenamiento en Python")
    print("🎯 Usando matplotlib para visualizaciones interactivas")
    print("=" * 50)
    
    # Crear visualizador
    visualizer = LSTMTrainingVisualizer()
    
    # Mostrar todas las visualizaciones
    visualizer.show_all_visualizations()
    
    print("\n✅ Visualización completada")
    print("📁 Los gráficos se muestran en ventanas separadas")
    print("💡 Cierra las ventanas para terminar")

if __name__ == "__main__":
    main() 