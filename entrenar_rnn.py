import pandas as pd
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, SimpleRNN, TimeDistributed, Dense
from sklearn.model_selection import train_test_split
import pickle

df = pd.read_csv('historial_comandos.csv', header=None, names=['fecha', 'comando', 'respuesta'])
comandos = df['comando'].astype(str).values
respuestas = df['respuesta'].astype(str).values

num_palabras = 2000
maxlen = 20

tokenizer = Tokenizer(num_words=num_palabras, oov_token='<OOV>')
tokenizer.fit_on_texts(np.concatenate((comandos, respuestas)))

X = tokenizer.texts_to_sequences(comandos)
X = pad_sequences(X, maxlen=maxlen, padding='post')

y = tokenizer.texts_to_sequences(respuestas)
y = pad_sequences(y, maxlen=maxlen, padding='post')

# Convertir a one-hot
y_cat = to_categorical(y, num_classes=num_palabras)

X_train, X_test, y_train, y_test = train_test_split(X, y_cat, test_size=0.2, random_state=42)

def build_model():
    model = Sequential([
        Embedding(num_palabras, 64, input_length=maxlen),
        SimpleRNN(64, return_sequences=True),
        TimeDistributed(Dense(num_palabras, activation='softmax'))
    ])
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

model = build_model()

model.fit(X_train, y_train, epochs=30, batch_size=8, validation_data=(X_test, y_test))

model.save('modelo_rnn_comandos.h5')
with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
print('Entrenamiento finalizado y modelo guardado.')
