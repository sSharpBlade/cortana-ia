import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Embedding
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import pickle
import json
import os
from datetime import datetime
import sqlite3
import re
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

class AngieLSTMTrainer:
    def __init__(self, db_path='angie_data.db', max_words=1000, max_len=50):
        self.db_path = db_path
        self.max_words = max_words
        self.max_len = max_len
        self.tokenizer = Tokenizer(num_words=max_words, oov_token='<OOV>')
        self.label_encoder = LabelEncoder()
        self.scaler = StandardScaler()
        self.model = None
        self.history = None
        
        # Configurar matplotlib para mejor visualización
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
    def load_interaction_data(self):
        """Cargar datos de interacciones desde la base de datos"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Crear tabla de interacciones si no existe
            conn.execute('''
                CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_input TEXT NOT NULL,
                    assistant_response TEXT NOT NULL,
                    command_type TEXT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    confidence REAL DEFAULT 0.0
                )
            ''')
            
            # Cargar datos existentes
            df = pd.read_sql_query("SELECT * FROM interactions", conn)
            conn.close()
            
            if df.empty:
                print("No hay datos de interacciones. Generando datos de ejemplo...")
                df = self.generate_sample_data()
                
            return df
            
        except Exception as e:
            print(f"Error cargando datos: {e}")
            return self.generate_sample_data()
    
    def generate_sample_data(self):
        """Generar datos de ejemplo para demostración"""
        sample_data = {
            'user_input': [
                "¿qué hora es?",
                "dime el clima",
                "busca información sobre python",
                "reproduce música",
                "toma una nota",
                "captura de pantalla",
                "muestra información del sistema",
                "agrega un recordatorio",
                "¿cómo estás?",
                "cuéntame un chiste",
                "busca noticias",
                "abre google",
                "¿qué día es hoy?",
                "reproduce en spotify",
                "muestra mis tareas"
            ],
            'assistant_response': [
                "Son las 3:45 PM",
                "El clima actual es soleado con 25°C",
                "Python es un lenguaje de programación...",
                "Reproduciendo música en YouTube",
                "Ventana de notas abierta",
                "Captura de pantalla guardada",
                "CPU: 45%, RAM: 60%, Disco: 70%",
                "Recordatorio agregado exitosamente",
                "¡Hola! Estoy funcionando perfectamente",
                "¿Por qué los programadores prefieren el frío? Porque odian los bugs",
                "Aquí tienes las últimas noticias...",
                "Abriendo Google en tu navegador",
                "Hoy es lunes 15 de enero",
                "Reproduciendo en Spotify",
                "Tienes 3 tareas pendientes"
            ],
            'command_type': [
                'time', 'weather', 'search', 'music', 'notes',
                'screenshot', 'system', 'reminder', 'chat', 'chat',
                'news', 'navigation', 'time', 'music', 'tasks'
            ]
        }
        
        df = pd.DataFrame(sample_data)
        df['timestamp'] = pd.Timestamp.now()
        df['confidence'] = np.random.uniform(0.7, 1.0, len(df))
        
        return df
    
    def preprocess_data(self, df):
        """Preprocesar datos para entrenamiento"""
        # Limpiar texto
        df['user_input_clean'] = df['user_input'].apply(self.clean_text)
        
        # Tokenizar texto
        self.tokenizer.fit_on_texts(df['user_input_clean'])
        sequences = self.tokenizer.texts_to_sequences(df['user_input_clean'])
        X = pad_sequences(sequences, maxlen=self.max_len)
        
        # Codificar etiquetas
        y = self.label_encoder.fit_transform(df['command_type'])
        
        return X, y, df['command_type'].unique()
    
    def clean_text(self, text):
        """Limpiar y normalizar texto"""
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def create_lstm_model(self, num_classes, vocab_size):
        """Crear modelo LSTM con 2-3 capas"""
        model = Sequential([
            Embedding(vocab_size, 128, input_length=self.max_len),
            LSTM(128, return_sequences=True, dropout=0.2),
            LSTM(64, return_sequences=True, dropout=0.2),
            LSTM(32, dropout=0.2),
            Dense(64, activation='relu'),
            Dropout(0.3),
            Dense(num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def train_model(self, X, y, epochs=50, batch_size=32):
        """Entrenar el modelo LSTM"""
        # Dividir datos
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Crear modelo
        vocab_size = len(self.tokenizer.word_index) + 1
        num_classes = len(np.unique(y))
        self.model = self.create_lstm_model(num_classes, vocab_size)
        
        # Callbacks
        early_stopping = EarlyStopping(
            monitor='val_loss', patience=10, restore_best_weights=True
        )
        reduce_lr = ReduceLROnPlateau(
            monitor='val_loss', factor=0.5, patience=5, min_lr=1e-7
        )
        
        # Entrenar
        self.history = self.model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=(X_test, y_test),
            callbacks=[early_stopping, reduce_lr],
            verbose=1
        )
        
        # Evaluar
        y_pred = np.argmax(self.model.predict(X_test), axis=1)
        accuracy = accuracy_score(y_test, y_pred)
        
        return X_test, y_test, y_pred, accuracy
    
    def generate_training_visualizations(self, X_test, y_test, y_pred, accuracy, df):
        """Generar visualizaciones del entrenamiento"""
        # Crear directorio para gráficos
        os.makedirs('training_plots', exist_ok=True)
        
        # 1. Gráfico de pérdida y precisión durante el entrenamiento
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        ax1.plot(self.history.history['loss'], label='Pérdida de Entrenamiento', linewidth=2)
        ax1.plot(self.history.history['val_loss'], label='Pérdida de Validación', linewidth=2)
        ax1.set_title('Evolución de la Pérdida', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Época')
        ax1.set_ylabel('Pérdida')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        ax2.plot(self.history.history['accuracy'], label='Precisión de Entrenamiento', linewidth=2)
        ax2.plot(self.history.history['val_accuracy'], label='Precisión de Validación', linewidth=2)
        ax2.set_title('Evolución de la Precisión', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Época')
        ax2.set_ylabel('Precisión')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('training_plots/training_curves.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # 2. Matriz de confusión
        cm = confusion_matrix(y_test, y_pred)
        class_names = self.label_encoder.classes_
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=class_names, yticklabels=class_names)
        plt.title('Matriz de Confusión', fontsize=16, fontweight='bold')
        plt.xlabel('Predicción', fontsize=12)
        plt.ylabel('Valor Real', fontsize=12)
        plt.xticks(rotation=45)
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.savefig('training_plots/confusion_matrix.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # 3. Distribución de comandos
        plt.figure(figsize=(12, 6))
        command_counts = df['command_type'].value_counts()
        colors = plt.cm.Set3(np.linspace(0, 1, len(command_counts)))
        
        bars = plt.bar(range(len(command_counts)), command_counts.values, color=colors)
        plt.title('Distribución de Tipos de Comandos', fontsize=16, fontweight='bold')
        plt.xlabel('Tipo de Comando', fontsize=12)
        plt.ylabel('Frecuencia', fontsize=12)
        plt.xticks(range(len(command_counts)), command_counts.index, rotation=45)
        
        # Agregar valores en las barras
        for bar, count in zip(bars, command_counts.values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    str(count), ha='center', va='bottom', fontweight='bold')
        
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.savefig('training_plots/command_distribution.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # 4. Análisis de longitud de comandos
        df['input_length'] = df['user_input'].str.len()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # Histograma de longitudes
        ax1.hist(df['input_length'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        ax1.set_title('Distribución de Longitud de Comandos', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Longitud del Comando')
        ax1.set_ylabel('Frecuencia')
        ax1.grid(True, alpha=0.3)
        
        # Box plot por tipo de comando
        df.boxplot(column='input_length', by='command_type', ax=ax2)
        ax2.set_title('Longitud de Comandos por Tipo', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Tipo de Comando')
        ax2.set_ylabel('Longitud')
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('training_plots/command_length_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # 5. Palabras más frecuentes
        all_words = ' '.join(df['user_input_clean']).split()
        word_freq = Counter(all_words)
        top_words = dict(word_freq.most_common(15))
        
        plt.figure(figsize=(12, 6))
        words = list(top_words.keys())
        frequencies = list(top_words.values())
        
        bars = plt.barh(range(len(words)), frequencies, color='lightcoral')
        plt.title('Palabras Más Frecuentes en Comandos', fontsize=16, fontweight='bold')
        plt.xlabel('Frecuencia', fontsize=12)
        plt.ylabel('Palabras', fontsize=12)
        plt.yticks(range(len(words)), words)
        
        # Agregar valores en las barras
        for i, (bar, freq) in enumerate(zip(bars, frequencies)):
            plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                    str(freq), ha='left', va='center', fontweight='bold')
        
        plt.grid(True, alpha=0.3, axis='x')
        plt.tight_layout()
        plt.savefig('training_plots/word_frequency.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # 6. Resumen de métricas
        self.create_metrics_summary(accuracy, df)
        
        return {
            'accuracy': accuracy,
            'confusion_matrix': cm,
            'class_names': class_names,
            'training_history': self.history.history
        }
    
    def create_metrics_summary(self, accuracy, df):
        """Crear resumen de métricas"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # Métricas principales
        metrics_data = {
            'Precisión': [accuracy * 100],
            'Total Comandos': [len(df)],
            'Tipos Únicos': [df['command_type'].nunique()],
            'Palabras Únicas': [len(set(' '.join(df['user_input_clean']).split()))]
        }
        
        metrics_df = pd.DataFrame(metrics_data)
        ax1.bar(metrics_df.columns, metrics_df.iloc[0], color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
        ax1.set_title('Métricas Principales', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Valor')
        ax1.tick_params(axis='x', rotation=45)
        
        # Agregar valores en las barras
        for i, v in enumerate(metrics_df.iloc[0]):
            ax1.text(i, v + max(metrics_df.iloc[0]) * 0.01, f'{v:.1f}', 
                    ha='center', va='bottom', fontweight='bold')
        
        # Precisión por época
        ax2.plot(self.history.history['accuracy'], label='Entrenamiento', linewidth=2)
        ax2.plot(self.history.history['val_accuracy'], label='Validación', linewidth=2)
        ax2.set_title('Precisión por Época', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Época')
        ax2.set_ylabel('Precisión')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Pérdida por época
        ax3.plot(self.history.history['loss'], label='Entrenamiento', linewidth=2)
        ax3.plot(self.history.history['val_loss'], label='Validación', linewidth=2)
        ax3.plot(self.history.history['val_loss'], label='Validación', linewidth=2)
        ax3.set_title('Pérdida por Época', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Época')
        ax3.set_ylabel('Pérdida')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Distribución temporal (simulada)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        hourly_counts = df['hour'].value_counts().sort_index()
        
        ax4.plot(hourly_counts.index, hourly_counts.values, marker='o', linewidth=2, markersize=8)
        ax4.set_title('Actividad por Hora del Día', fontsize=14, fontweight='bold')
        ax4.set_xlabel('Hora')
        ax4.set_ylabel('Número de Comandos')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('training_plots/metrics_summary.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def save_model(self, filename='angie_lstm_model'):
        """Guardar modelo entrenado"""
        if self.model is not None:
            # Guardar modelo
            self.model.save(f'{filename}.h5')
            
            # Guardar tokenizer y encoders
            with open(f'{filename}_tokenizer.pkl', 'wb') as f:
                pickle.dump(self.tokenizer, f)
            
            with open(f'{filename}_label_encoder.pkl', 'wb') as f:
                pickle.dump(self.label_encoder, f)
            
            print(f"Modelo guardado como {filename}.h5")
    
    def load_model(self, filename='angie_lstm_model'):
        """Cargar modelo entrenado"""
        try:
            self.model = tf.keras.models.load_model(f'{filename}.h5')
            
            with open(f'{filename}_tokenizer.pkl', 'rb') as f:
                self.tokenizer = pickle.load(f)
            
            with open(f'{filename}_label_encoder.pkl', 'rb') as f:
                self.label_encoder = pickle.load(f)
            
            print("Modelo cargado exitosamente")
            return True
        except Exception as e:
            print(f"Error cargando modelo: {e}")
            return False
    
    def predict_command_type(self, text):
        """Predecir tipo de comando para nuevo texto"""
        if self.model is None:
            return "Modelo no entrenado"
        
        # Preprocesar texto
        clean_text = self.clean_text(text)
        sequence = self.tokenizer.texts_to_sequences([clean_text])
        padded = pad_sequences(sequence, maxlen=self.max_len)
        
        # Predecir
        prediction = self.model.predict(padded)
        predicted_class = np.argmax(prediction[0])
        confidence = np.max(prediction[0])
        
        return {
            'command_type': self.label_encoder.classes_[predicted_class],
            'confidence': confidence,
            'all_probabilities': dict(zip(self.label_encoder.classes_, prediction[0]))
        }
    
    def run_full_training(self):
        """Ejecutar entrenamiento completo con visualizaciones"""
        print("🚀 Iniciando entrenamiento LSTM para Angie...")
        
        # Cargar datos
        print("📊 Cargando datos de interacciones...")
        df = self.load_interaction_data()
        print(f"✅ Datos cargados: {len(df)} interacciones")
        
        # Preprocesar
        print("🔧 Preprocesando datos...")
        X, y, unique_commands = self.preprocess_data(df)
        print(f"✅ Datos preprocesados. Comandos únicos: {unique_commands}")
        
        # Entrenar
        print("🧠 Entrenando modelo LSTM...")
        X_test, y_test, y_pred, accuracy = self.train_model(X, y)
        print(f"✅ Entrenamiento completado. Precisión: {accuracy:.4f}")
        
        # Generar visualizaciones
        print("📈 Generando visualizaciones...")
        results = self.generate_training_visualizations(X_test, y_test, y_pred, accuracy, df)
        
        # Guardar modelo
        print("💾 Guardando modelo...")
        self.save_model()
        
        print("🎉 ¡Entrenamiento completado exitosamente!")
        print(f"📁 Visualizaciones guardadas en: training_plots/")
        print(f"📊 Precisión final: {accuracy:.2%}")
        
        return results

if __name__ == "__main__":
    # Ejecutar entrenamiento completo
    trainer = AngieLSTMTrainer()
    results = trainer.run_full_training()
