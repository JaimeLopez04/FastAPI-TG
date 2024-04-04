from email import message
from fastapi import File, Query, UploadFile, APIRouter, Response, Form
from datetime import datetime, timedelta
from sqlalchemy import and_
import json
import os

#Local libraries
from app.utils.functions.emotion_recognition import detect_faces_and_emotions
from app.models.class_taught import class_taught
from app.config.db import conn

emotions_recognizer = APIRouter(prefix='/api')


@emotions_recognizer.post("/emotion_recognizer/analyze_video")
async def analyze_video(file: UploadFile = File(...), id_user: str = Form(...), class_name: str = Form(...), class_date: str = Form(...)):
    videos_count = count_videos_in_directory('app/storage/videos')
    try:
        # Crear la ruta para guardar el video
        folder_path = os.path.join("app", "storage", "videos")
        os.makedirs(folder_path, exist_ok=True)
        video_name = f"{id_user}_{class_name}_{class_date}_{videos_count + 1}.mp4"
        video_path = os.path.join(folder_path, video_name)

        # Guardar el archivo de video en el sistema
        with open(video_path, "wb") as buffer:
            while True:
                # Leer en fragmentos pequeños para evitar la sobrecarga de memoria
                chunk = await file.read(10000)
                if not chunk:
                    break
                # Convertir a bytes si es str y luego escribir en el archivo
                if isinstance(chunk, str):
                    chunk = chunk.encode()
                buffer.write(chunk)

        # Realizar el análisis de emociones en el video
        emotions_detected = detect_faces_and_emotions(video_path)
        
        if emotions_detected['dominan_emotion'] not in ['Felicidad', 'Sorpresa', 'Neutral']:
            message = json.dumps({
                "emotions_detected": emotions_detected,
                "status_code": 200,
                "video_link": f"/download/{video_name}"  # Ruta para descargar el video
            })
            
            await save_class(id_user, video_path, class_name, class_date, emotions_detected)
            
            return Response(content=message, media_type="application/json", status_code=200)
        else :
            os.remove(video_path)
            message = json.dumps({
                "message" : emotions_detected,
                "status_code" : 200
            })
            
            await save_class(id_user, 'Sin video', class_name, class_date, emotions_detected)
            
            return Response(content=message, media_type='application/json', status_code=200)
            
    except Exception as e:
        message = json.dumps({
            "error" : str(e),
            "status_code" : 422
        })
        return Response(content=message, media_type="application/json", status_code=422)


async def save_class(id_user, filePath, class_name, class_date, emotions_detected):
    new_class = {
        "class_name" : class_name,
        "class_date" : class_date,
        "id_user" : id_user,
        "enojo" : emotions_detected.enojo,
        "disgusto" : emotions_detected.disgusto,
        "miedo" : emotions_detected.miedo,
        "felicidad" : emotions_detected.felicidad,
        "tristeza" : emotions_detected.tristeza,
        "sorpresa" : emotions_detected.sorpresa,
        "neutral" : emotions_detected.neutral,
        "faces_detected" : emotions_detected.faces_detected,
        "dominant_emotion" : emotions_detected.dominant_emotion,
        "file_path" : filePath
    }
    
    # Insertar los datos de la clase en la base de datos
    conn.execute(class_taught.insert().values(new_class))
    # Guardar los cambios
    conn.commit()
    
    return


def count_videos_in_directory(directory):
    try:
        # Obtener la lista de archivos en el directorio
        files = os.listdir(directory)
        # Contador para contar los videos
        video_count = 0
        # Iterar sobre los archivos y contar los videos
        for file in files:
            # Verificar si el archivo es un video (puedes ajustar esto según la extensión de tus videos)
            if file.endswith(".mp4"):
                video_count += 1
        return video_count
    except Exception as e:
        print("Error al contar los videos:", e)
        return 0


# Crear la función para guardar el video
async def save_video(file, id_user, class_name, class_date):
    try:
        # Crear la ruta para guardar el video
        folder_path = os.path.join("app", "storage", "videos")
        os.makedirs(folder_path, exist_ok=True)
        video_name = f"{id_user}_{class_name}_{class_date}.mp4"
        video_path = os.path.join(folder_path, video_name)

        # Guardar el archivo de video en el sistema
        with open(video_path, "wb") as buffer:
            while True:
                # Leer en fragmentos pequeños para evitar la sobrecarga de memoria
                chunk = await file.read(10000)
                if not chunk:
                    break
                # Convertir a bytes si es str y luego escribir en el archivo
                if isinstance(chunk, str):
                    chunk = chunk.encode()
                buffer.write(chunk)

        return video_path  # Devolver la ruta del video guardado
    except Exception as e:
        print("Error al guardar el video:", e)
        return None
    
    
@emotions_recognizer.get('/emotion_recognizer/get_resumen')
def get_resumen(id_user: str = Query(...)):
    
    # Obtener la fecha del primer día de la semana (lunes)
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())

    # Obtener la fecha del último día de la semana (domingo)
    end_of_week = start_of_week + timedelta(days=6)

    # Filtrar los registros por la fecha de la clase que esté entre el lunes y el domingo de esta semana
    resumen = conn.execute(
        class_taught.select().where(
            and_(
                class_taught.c.id_user == id_user,
                class_taught.c.class_date >= start_of_week.date(),
                class_taught.c.class_date <= end_of_week.date()
            )
        )
    ).all()
    
    message = json.dumps({
        "emotions_resume" : resumen,
        "status_code" : 200
    })
    
    return Response(content=message, media_type='application/json', status_code=200)