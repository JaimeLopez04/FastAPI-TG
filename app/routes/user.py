from fastapi import APIRouter
from ..models.user import users
from ..config.db import conn


user = APIRouter(prefix='/api')

@user.get('/users')
def get_users():
    return conn.execute(users.select()).fetchall()