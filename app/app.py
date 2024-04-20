'''Inicializador de la aplicación'''

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

#local Files
from .routes.recognizer import emotions_recognizer
from .routes.user import user

app = FastAPI()

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# Ruta estática para la carpeta de videos
app.mount("/storage/videos", StaticFiles(directory="app/storage/videos"), name="videos")

# Incluye todos los enrutadores en la aplicación
app.include_router(user)
app.include_router(emotions_recognizer)

