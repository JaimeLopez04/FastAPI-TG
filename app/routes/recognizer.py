from fastapi import File, Query, UploadFile, APIRouter, Response, Form
from datetime import datetime, timedelta
from sqlalchemy import and_
from sqlalchemy.sql.expression import insert  # Importa el método insert
from collections import Counter
import json
import os

#Local libraries
from app.utils.functions.emotion_recognition import detect_faces_and_emotions
from app.models.class_taught import class_taught
from app.config.db import conn

emotions_recognizer = APIRouter(prefix='/api')


@emotions_recognizer.post("/emotion_recognizer/analyze_video")
async def analyze_video(file: UploadFile = File(...), id_user: int = Form(...), class_name: str = Form(...), class_date: str = Form(...)):
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
        if 'dominan_emotion' in emotions_detected and emotions_detected['dominan_emotion'] not in ['Felicidad', 'Sorpresa', 'Neutral']:
            message = {
                "emotions_detected": emotions_detected,
                "status_code": 200,
                "video_link": f"/download/{video_name}"  # Ruta para descargar el video
            }
            await save_class(id_user, video_path, class_name, class_date, emotions_detected)
            return Response(content=json.dumps(message), media_type="application/json", status_code=200)
        else:
            os.remove(video_path)
            message = {
                "message": emotions_detected,
                "status_code": 200
            }
            await save_class(id_user, 'Sin video', class_name, class_date, emotions_detected)
            return Response(content=json.dumps(message), media_type='application/json', status_code=200)
    except Exception as e:
        message = {
            "error": str(e),
            "status_code": 422
        }
        return Response(content=json.dumps(message), media_type="application/json", status_code=422)


async def save_class(id_user, file_path, class_name, class_date, emotions_detected):

    try:
        new_class = {
            "class_name": class_name,
            "class_date": class_date,
            "id_user": id_user,
            "enojo": emotions_detected['emotions_detected'].get('Enojo', 0),
            "disgusto": emotions_detected['emotions_detected'].get('Disgusto', 0),
            "miedo": emotions_detected['emotions_detected'].get('Miedo', 0),
            "felicidad": emotions_detected['emotions_detected'].get('Felicidad', 0),
            "tristeza": emotions_detected['emotions_detected'].get('Tristeza', 0),
            "sorpresa": emotions_detected['emotions_detected'].get('Sorpresa', 0),
            "neutral": emotions_detected['emotions_detected'].get('Neutral', 0),
            "faces_detected": emotions_detected.get('faces_detected', 0),
            "dominant_emotion": emotions_detected.get('dominan_emotion', 'Desconocido'),
            "file_path": file_path
        }

        
        # Insertar los datos de la clase en la base de datos
        conn.execute(insert(class_taught).values(new_class))
        # Guardar los cambios
        conn.commit()
    except Exception as e:
        print("Error al guardar en la base de datos:", str(e))
        raise

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


# @emotions_recognizer.get('/emotion_recognizer/get_resumen')
# def get_resumen(id_user: str = Query(...)):
#     print(f'Si entra aquí {id_user}')
#     print(type(id_user))
    
#     # Obtener la fecha del primer día de la semana (lunes)
#     today = datetime.now()
#     start_of_week = today - timedelta(days=today.weekday())

#     # Obtener la fecha del último día de la semana (domingo)
#     end_of_week = start_of_week + timedelta(days=6)

#     # Filtrar los registros por la fecha de la clase que esté entre el lunes y el domingo de esta semana
#     resumen = conn.execute(
#         class_taught.select().where(
#             and_(
#                 class_taught.c.id_user == id_user,
#                 class_taught.c.class_date >= start_of_week.date(),
#                 class_taught.c.class_date <= end_of_week.date()
#             )
#         )
#     ).all()
    
#     if not resumen:
#         #No hay datos retorna
#         response_content = json.dumps({"message": "Aún no tienes datos registrados", "status_code": 200})
#         return Response(content=response_content, media_type='application/json', status_code=200)

#     # Calcular las sumas de las emociones y el total de faces detectadas
#     sum_emojos = sum(row[4] for row in resumen)
#     sum_disgusto = sum(row[5] for row in resumen)
#     sum_miedo = sum(row[6] for row in resumen)
#     sum_felicidad = sum(row[7] for row in resumen)
#     sum_tristeza = sum(row[8] for row in resumen)
#     sum_sorpresa = sum(row[9] for row in resumen)
#     sum_neutral = sum(row[10] for row in resumen)
#     total_faces_detected = sum(row[11] for row in resumen)

#     # Contar cuántas veces aparece cada emoción predominante
#     dominant_emotions_counter = Counter(row[12] for row in resumen)

#     # Encontrar la emoción predominante más común
#     dominant_emotion_most_common = dominant_emotions_counter.most_common(1)[0][0]

#     # Crear un diccionario con los totales de emociones y faces detectadas
#     emotions_totals = {
#         "enojo": sum_emojos,
#         "disgusto": sum_disgusto,
#         "miedo": sum_miedo,
#         "felicidad": sum_felicidad,
#         "tristeza": sum_tristeza,
#         "sorpresa": sum_sorpresa,
#         "neutral": sum_neutral,
#         "total_faces_detected": total_faces_detected,
#         "most_dominant_emotion": dominant_emotion_most_common
#     }

#     # Crear la respuesta JSON
#     response_content = json.dumps({"emotions_totals": emotions_totals, "status_code": 200})

#     # Retorna la respuesta con el contenido JSON y el código de estado 200
#     return Response(content=response_content, media_type='application/json', status_code=200)

@emotions_recognizer.get('/emotion_recognizer/get_resumen')
def get_resumen(id_user: str = Query(...)):
    print(f'Si entra aquí {id_user}')
    print(type(id_user))
    
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
    
    if not resumen:
        # No hay datos, retorna un mensaje indicando que no hay datos registrados
        response_content = json.dumps({"message": "Aún no tienes datos registrados", "status_code": 200})
        return Response(content=response_content, media_type='application/json', status_code=200)

    # Inicializa las variables de suma de emociones y total de caras detectadas
    sum_emojos = 0
    sum_disgusto = 0
    sum_miedo = 0
    sum_felicidad = 0
    sum_tristeza = 0
    sum_sorpresa = 0
    sum_neutral = 0
    total_faces_detected = 0

    # Itera sobre los registros y realiza las sumas
    for row in resumen:
        sum_emojos += row[4]
        sum_disgusto += row[5]
        sum_miedo += row[6]
        sum_felicidad += row[7]
        sum_tristeza += row[8]
        sum_sorpresa += row[9]
        sum_neutral += row[10]
        total_faces_detected += row[11]

    # Contar cuántas veces aparece cada emoción predominante
    dominant_emotions_counter = Counter(row[12] for row in resumen)

    # Encontrar la emoción predominante más común
    dominant_emotion_most_common = dominant_emotions_counter.most_common(1)[0][0]

    # Crear un diccionario con los totales de emociones y faces detectadas
    emotions_totals = {
        "enojo": sum_emojos,
        "disgusto": sum_disgusto,
        "miedo": sum_miedo,
        "felicidad": sum_felicidad,
        "tristeza": sum_tristeza,
        "sorpresa": sum_sorpresa,
        "neutral": sum_neutral,
        "total_faces_detected": total_faces_detected,
        "most_dominant_emotion": dominant_emotion_most_common
    }

    # Crear la respuesta JSON
    response_content = json.dumps({"emotions_totals": emotions_totals, "status_code": 200})

    # Retorna la respuesta con el contenido JSON y el código de estado 200
    return Response(content=response_content, media_type='application/json', status_code=200)