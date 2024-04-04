from sqlalchemy import ForeignKey, Table, Column, String, Integer
from ..config.db import meta, engine

class_taught = Table('class_taught', meta,
                Column('id_class', Integer,
                        primary_key=True, autoincrement=True),
                Column('class_name', String(255)),
                Column('class_date', String(255)),
                Column('id_user', String(255),
                        ForeignKey('users.id_user')),
                Column('enojo', Integer),
                Column('disgusto', Integer),
                Column('miedo', Integer),
                Column('felicidad', Integer),
                Column('tristeza', Integer),
                Column('sorpresa', Integer),
                Column('neutral', Integer),
                Column('faces_detected', Integer),
                Column('dominant_emotion', String(255)),
                Column('file_path', String(255), unique=True)
                )

meta.create_all(engine)
