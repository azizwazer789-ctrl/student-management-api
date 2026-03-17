from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from typing import List

from models import Student, StudentResponse, UserLogin
from database import students_db
from auth import authenticate_user

from fastapi import FastAPI
from database import Base, engine
from routes import student

from sqlalchemy import Column, Integer, String
# No dot here! This is an absolute import.
from database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    course = Column(String)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Management API")
app.include_router(student.router)


# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):

    return JSONResponse(
        status_code=500,
        content={
            "message": "Unexpected server error",
            "detail": str(exc)
        }
    )


# Login API
@app.post("/login")
def login(user: UserLogin):

    authenticate_user(user.username, user.password)

    return {"message": "Login successful"}


# Create Student
@app.post("/students", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: Student):

    for s in students_db:
        if s["id"] == student.id:
            raise HTTPException(
                status_code=400,
                detail="Student ID already exists"
            )

    students_db.append(student.dict())

    return {
        "message": "Student created successfully",
        "student": student
    }


# Get All Students
@app.get("/students", response_model=List[Student])
def get_students():

    return students_db


# Get Single Student
@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):

    for student in students_db:
        if student["id"] == student_id:
            return student

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )


# Delete Student
@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    for student in students_db:
        if student["id"] == student_id:
            students_db.remove(student)
            return {"message": "Student deleted successfully"}

    raise HTTPException(
        status_code=404,
        detail="Student not found"
)