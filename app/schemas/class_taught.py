from pydantic import BaseModel
from typing import Optional

class ClassTaught(BaseModel):
    id_class: Optional[str]
    class_name: str
    class_date: str
    id_user: int
    enojo: int
    disgusto: int
    miedo: int
    felicidad: int
    tristeza: int
    sorpresa: int
    neutral: int
    face_detected: int
    dominant_emotion: str
    file_path: str


class GetInformation(BaseModel):
    id_user: str
