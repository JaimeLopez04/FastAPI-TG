import cv2
from keras.models import load_model
import numpy as np

emotion_labels = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Sad', 5: 'Surprise', 6: 'Neutral'}

# Cargar el modelo de análisis de sentimientos
emotion_model = load_model('app/utils/models/emotion_model.h5')

def detect_faces_and_emotions(video_path):
    # Cargar el clasificador Haar Cascade para la detección de rostros
    face_cascade = cv2.CascadeClassifier('app/utils/models/haarcascade_frontalface_default.xml')

    # Iniciar la captura de video
    cap = cv2.VideoCapture(video_path)

    emotions_detected = {emotion_label: 0 for emotion_label in emotion_labels.values()}
    total_faces = 0

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detectar rostros en la imagen
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face = gray[y:y + h, x:x + w]

            # Preprocesar la imagen para el modelo de emociones
            face = cv2.resize(face, (48, 48))
            face = np.expand_dims(face, axis=0)
            face = face / 255.0

            # Predecir la emoción
            emotion_pred = emotion_model.predict(face)[0]
            emotion_label = emotion_labels[np.argmax(emotion_pred)]
            emotions_detected[emotion_label] += 1
            total_faces += 1

    # Liberar recursos
    cap.release()
    cv2.destroyAllWindows()

    # Calcular el porcentaje de cada emoción
    emotions_percentage = {emotion_label: (count / total_faces) * 100 for emotion_label, count in emotions_detected.items()}

    return emotions_detected, emotions_percentage
