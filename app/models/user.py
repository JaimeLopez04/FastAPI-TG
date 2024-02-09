from sqlalchemy import Table, Column, String, Integer, Boolean, column, true
from ..config.db import meta, engine

users = Table('users', meta,
            Column('id_user', Integer, primary_key=True, autoincrement=True),
            Column('user_names', String(255)),
            Column('user_last_name', String(255)),
            Column('email', String(255)),
            Column('password', String(255))
            )

meta.create_all(engine)