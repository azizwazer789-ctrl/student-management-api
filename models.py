from pydantic import BaseModel, Field

class Student(BaseModel):
    id: int
    name: str = Field(..., min_length=2)
    age: int = Field(..., gt=15)
    course: str


class StudentResponse(BaseModel):
    message: str
    student: Student


class UserLogin(BaseModel):
    username: str
    password: str