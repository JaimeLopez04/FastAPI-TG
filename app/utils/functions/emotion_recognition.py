import cv2
from keras.models import load_model
import numpy as np
import concurrent.futures

emotion_labels = {0: 'Enojo', 1: 'Disgusto', 2: 'Miedo',
                  3: 'Felicidad', 4: 'Tristeza', 5: 'Sorpresa', 6: 'Neutral'}

def predict_emotion(face, emotion_model):
    face = cv2.resize(face, (48, 48))
    face = np.expand_dims(face, axis=0)
    face = face.astype('float32') / 255.0
    emotion_pred = np.argmax(emotion_model.predict(face))
    return emotion_labels[emotion_pred]

def detect_faces_and_emotions(video_path):
    try:
        emotion_model = load_model('app/utils/models/emotion_model.h5')
    except OSError as e:
        print("Error cargando el modelo de emociones:", e)
        return {"error": "Modelo de emociones no cargado"}

    if emotion_model is None:
        print("El modelo de emociones no se cargó correctamente.")
        return {"error": "Modelo de emociones no cargado"}

    face_cascade = cv2.CascadeClassifier('app/utils/models/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(video_path)

    emotions_detected = {emotion_label: 0 for emotion_label in emotion_labels.values()}
    total_faces = 0

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                face = gray[y:y + h, x:x + w]
                futures.append(executor.submit(predict_emotion, face, emotion_model))
                total_faces += 1

        for future in concurrent.futures.as_completed(futures):
            emotion_pred = future.result()
            emotions_detected[emotion_pred] += 1

    # Encontrar la emoción predominante
    emotion_pred = max(emotions_detected.items(), key=lambda x: x[1])[0]
    return {
        "emotions_detected": emotions_detected,
        "faces_detected": total_faces,
        "dominan_emotion": emotion_pred
    }

