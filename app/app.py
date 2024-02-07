from fastapi import FastAPI

app = FastAPI()

#app.include_router(user) TO USE ROUTES

@app.get('/')
def get_method():
    return 'Funtion get'