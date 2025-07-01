import speech_recognition as sr
import pyttsx3
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

model = load_model('modelo_rnn_comandos.h5')
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

maxlen = 20
num_palabras = 2000

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        try:
            rec = r.recognize_google(audio, language='es-ES').lower()
            return rec
        except:
            return ""

def predecir_respuesta(comando):
    seq = tokenizer.texts_to_sequences([comando])
    seq = pad_sequences(seq, maxlen=maxlen, padding='post')
    pred = model.predict(seq)
    pred_indices = np.argmax(pred, axis=2)[0]  # shape: (maxlen,)
    # Decodificar a texto, omitir ceros y <OOV>
    index_word = {v: k for k, v in tokenizer.word_index.items()}
    respuesta = []
    for idx in pred_indices:
        if idx == 0 or idx == tokenizer.word_index.get('<OOV>', -1):
            continue
        palabra = index_word.get(idx, '')
        if palabra:
            respuesta.append(palabra)
    return ' '.join(respuesta)

def main():
    print("Asistente RNN listo. Di tu comando (di 'salir' para terminar):")
    while True:
        comando = get_audio()
        if not comando:
            continue
        if 'salir' in comando:
            speak('Hasta luego')
            break
        respuesta = predecir_respuesta(comando)
        print(f"Usuario: {comando}")
        print(f"Asistente: {respuesta}")
        speak(respuesta)

if __name__ == "__main__":
    main()
