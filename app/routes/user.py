#Import FastAPI modules and Python Modules
from fastapi import APIRouter, HTTPException
from cryptography.fernet import Fernet
from fastapi.responses import JSONResponse

#Import local files
from ..models.user import users
from ..config.db import conn
from ..schemas.user import User

#Crypt Pass
key = Fernet.generate_key()
f = Fernet(key)

#Route with defaul prefix /api to make route that /api/users etc...
user = APIRouter(prefix='/api')

@user.get('/users')
def get_users():
    try:
        # Realiza la consulta a la base de datos y obtiene las filas
        result_proxy = conn.execute(users.select())
        rows = result_proxy.fetchall()
        
        # Obtiene los nombres de las columnas de la tabla
        columns = result_proxy.keys()

        # Convierte las filas en una lista de diccionarios
        results = [dict(zip(columns, row)) for row in rows]
        
        # Devuelve los resultados en forma de JSON
        return results
    except Exception as e:
        # En caso de error, registra el error y lanza una excepción HTTP
        print("Error al obtener usuarios:", e)
        raise HTTPException(status_code=500, detail="Error al obtener usuarios")




@user.post('/create_user')
def create_user(user: User):
    try:
        # Crea un diccionario con los datos del nuevo usuario
        new_user = {
            "user_names": user.user_names,
            "user_last_names": user.user_last_names,
            "email": user.email,
            "password": f.encrypt(user.password.encode('utf-8')).decode('utf-8')
        }
        # Inserta los datos del nuevo usuario en la base de datos
        res = conn.execute(users.insert().values(new_user))
        # Confirma los cambios en la base de datos
        conn.commit()
        
        # Devuelve un mensaje de éxito junto con el ID del nuevo usuario
        return {"message": "Usuario creado exitosamente"}
    except Exception as e:
        # En caso de error, registra el error y lanza una excepción HTTP
        print("Error al crear usuario:", e)
        raise HTTPException(status_code=500, detail="Error al crear usuario")
