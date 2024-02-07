# from fastapi import APIRouter
# from ..config.db import conn
# from models.user import users

# user = APIRouter(prefix='/api')


# @user.get('/get_users')
# def guet_users():
#     return  conn.execute(users.select().fetch_all())