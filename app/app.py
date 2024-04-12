from fastapi import FastAPI
from .routes.user import user
from .routes.recognizer import emotions_recognizer
from fastapi.middleware.cors import CORSMiddleware

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

# Incluye todos los enrutadores en la aplicación
app.include_router(user)
app.include_router(emotions_recognizer)
