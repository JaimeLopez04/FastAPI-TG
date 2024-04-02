#Import FastAPI modules and Python Modules
from fastapi import APIRouter, Response, UploadFile, File
import json

#Emotion recongnizer funtion
from ..utils.functions.emotion_recognition import detect_faces_and_emotions

#Route with defaul prefix /api to make route that /api/emotion_recognizer etc...
emotions_recognizer = APIRouter(prefix='/api')

@emotions_recognizer.post("/analyze_video/")
async def analyze_video(file: UploadFile = File(...)):
    # Guardar el archivo de video en el sistema
    with open("video.mp4", "wb") as buffer:
        buffer.write(await file.read())

    # Realizar el análisis de emociones en el video
    emotions_detected, emotions_percentage = detect_faces_and_emotions("video.mp4")
    message = { "emotions_detected": emotions_detected, "emotions_percentage": emotions_percentage }

    return Response(content=json.dumps(message), media_type='application/json', status_code=200)
