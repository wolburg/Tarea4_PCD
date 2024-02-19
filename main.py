from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import uvicorn

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class User(BaseModel):
    user_name: str = Field(min_length=1)
    user_id: int = Field(min_length=1, max_length=100)
    user_email: str = Field(min_length=1, max_length=5000)
    age: int = Field(min_length=1)
    recommendations: list[str] = Field(default_factory=list)
    ZIP: str = Field(min_length=1, max_length=5000)

USERS = []

@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Users).all()

#Endpoint para crear un Usuario
@app.post("/")
def create_user(user: User, db: Session = Depends(get_db)):
    user_model = models.Users()
    user_model.name = user.name
    user_model.id = user.id
    user_model.email = user.email
    user_model.age = user.age
    user_model.recommendations = user.recommendations
    user_model.ZIP = user.ZIP

    db.add(user_model)
    db.commit()

    return user

#Endpoin actualiza el  user y que el email no se repita
@app.put("/{user_email}")
def update_user(user_email: int, user: User, db: Session = Depends(get_db)):

    user_model = db.query(models.Users).filter(models.Users.email == user_email).first()

    if user_model:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user_model.name = user.name
    user_model.id = user.id
    user_model.email = user.email
    user_model.age = user.age
    user_model.recommendations = user.recommendations
    user_model.ZIP = user.ZIP

    db.add(user_model)
    db.commit()

    return user

# Endpoint para actualizar un usuario por su ID
@app.put("/{user_id}")
def update_user(user_id: int, user: User, db: Session = Depends(get_db)):
    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID {user_id} not found"
        )
    # Actualizar los campos del usuario con los datos proporcionados
    user_model.user_name = user.user_name
    user_model.user_email = user.user_email
    user_model.age = user.age
    user_model.recommendations = user.recommendations
    user_model.ZIP = user.ZIP

    db.commit()
    return user_model

# Endpoint para obtener un usuario por su ID
@app.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID {user_id} not found"
        )
    return user_model

#Endpoint que elimina usruario
@app.delete("/{user_id}")
def delete_book(user_id: int, db: Session = Depends(get_db)):

    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {user_id} : Does not exist"
        )
    db.delete(user_model)
    db.commit()
    return {"message": "User deleted successfully"}

if __name__ == "__main__":
    uvicorn.run("books:app", host="0.0.0.0", port=5000, log_level="info",reload=True)
