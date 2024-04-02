#Import FastAPI modules and Python Modules
from fastapi import APIRouter, HTTPException, Response
import json

#Import local files
from ..models.user import users
from ..config.db import conn
from ..schemas.user import User, AuthUser


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

        # Convierte las filas en una lista de diccionarios y les da formato JSON
        results = json.dumps([dict(zip(columns, row)) for row in rows])
        
        if results == '[]' :
            message = {
                "message" : "No hay ningun usuario registrado actualmente"
            }
            return Response(content=json.dumps(message), media_type='application/json', status_code=200)
        
        # Devuelve los resultados en forma de JSON
        return Response(content=results, media_type='application/json', status_code=200)
    except Exception as e:
        print (e)
        # En caso de error, registra el error y lanza una excepción HTTP
        raise HTTPException(status_code=500, detail="Error al obtener usuarios")


@user.post('/create_user')
def create_user(user: User):
    try:
        # Crea un diccionario con los datos del nuevo usuario
        new_user = {
            "user_names": user.user_names,
            "user_last_names": user.user_last_names,
            "email": user.email,
            "password": user.password
        }
        #Verifica si el correo ya existe
        exits_user = conn.execute(users.select().where(users.c.email == new_user["email"])).first()

        #Si existe retorna una excepción
        if bool(exits_user):
            return HTTPException(status_code=422, detail="El correo ingresado ya se encuentra registrado")
        
        # Inserta los datos del nuevo usuario en la base de datos
        conn.execute(users.insert().values(new_user))
        # Confirma los cambios en la base de datos
        conn.commit()
        message = json.dumps({
            "message" : "¡Usuario registrado de manera exitosa!",
            "status_code" : 200
        })
        # Devuelve un mensaje de éxito junto con el ID del nuevo usuario
        return Response(content=message, media_type='application/json', status_code=200)
    except Exception as e:
        # En caso de error, registra el error y lanza una excepción HTTP
        raise HTTPException(status_code=500, detail="Error al crear usuario")
    

@user.post('/auth_user')
def authenticate(user: AuthUser):
    # Crea un diccionario con los datos del nuevo usuario
    auth_user = {
        "email": user.email,
        "password": user.password
    }
    
    result = conn.execute(users.select().where(users.c.email == auth_user["email"])).first()

    # Verificar si se encontró un usuario con ese correo electrónico
    if result is not None:
        password_from_db = result[4]  # Obtener la contraseña de la tupla
        names = result[1]
        last_names = result[2]
    else:
        message = json.dumps({
            "message" : "Tu usuario no fue encontrado",
            "status_code" : 422
        })
        return Response(content=message, media_type='application/json', status_code=422)
    
    if password_from_db == auth_user["password"]:
        message = json.dumps({
            "message" : f'{names} {last_names}',
            "status_code" : 200
        })
        return Response(content=message, media_type='application/json', status_code=200)
    else:
        message = json.dumps({
            "message" : "Tu contraseña es incorrecta",
            "status_code" : 422
        })
        return Response(content=message, media_type='application/json', status_code=422)
    
    
