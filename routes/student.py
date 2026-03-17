from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/students", response_model=schemas.StudentResponse)
def create(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db, student)

@router.get("/students")
def read(db: Session = Depends(get_db)):
    return crud.get_students(db)