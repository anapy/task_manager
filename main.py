from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
import models
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Mi gestor de tareas está funcionando 🚀"}


@app.post("/lists")
def create_list(list_data: schemas.ListCreate, db: Session = Depends(get_db)):
    new_list = models.List(name=list_data.name)

    db.add(new_list)
    db.commit()
    db.refresh(new_list)

    return new_list

@app.get("/lists", response_model=list[schemas.ListResponse])
def get_lists(db: Session = Depends(get_db)):
    return db.query(models.List).all()

@app.get("/lists/{list_id}", response_model=schemas.ListResponse)
def get_list(list_id: int, db: Session = Depends(get_db)):
    list_item = db.query(models.List).filter(models.List.id == list_id).first()

    if list_item is None:
        raise HTTPException(
            status_code=404,
            detail="Lista no encontrada"
        )

    return list_item

@app.put("/lists/{list_id}", response_model=schemas.ListResponse)
def update_list(
    list_id: int,
    list_data: schemas.ListUpdate,
    db: Session = Depends(get_db)
):
    list_item = db.query(models.List).filter(
        models.List.id == list_id
    ).first()

    if list_item is None:
        raise HTTPException(
            status_code=404,
            detail="Lista no encontrada"
        )

    list_item.name = list_data.name

    db.commit()
    db.refresh(list_item)

    return list_item

@app.delete("/lists/{list_id}")
def delete_list(list_id: int, db: Session = Depends(get_db)):
    list_item = db.query(models.List).filter(
        models.List.id == list_id
    ).first()

    if list_item is None:
        raise HTTPException(
            status_code=404,
            detail="Lista no encontrada"
        )

    db.delete(list_item)
    db.commit()

    return {
        "message": "Lista eliminada correctamente"
    }

@app.get("/tasks", response_model=list[schemas.TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()

@app.post("/tasks", response_model=schemas.TaskResponse)
def create_task(
    task_data: schemas.TaskCreate,
    db: Session = Depends(get_db)
):
    list_item = db.query(models.List).filter(
        models.List.id == task_data.list_id
    ).first()

    if list_item is None:
        raise HTTPException(
            status_code=404,
            detail="Lista no encontrada"
        )

    new_task = models.Task(
        title=task_data.title,
        description=task_data.description,
        list_id=task_data.list_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task_item = db.query(models.Task).filter(models.Task.id == task_id).first()

    if task_item is None:
        raise HTTPException(
            status_code=404,
            detail="Lista no encontrada"
        )

    return task_item

@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_list(
    task_id: int,
    task_data: schemas.TaskUpdate,
    db: Session = Depends(get_db)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Tarea no encontrada"
        )

    task.title = task_data.title
    task.description = task_data.description
    task.completed = task_data.completed

    db.commit()
    db.refresh(task)

    return task

@app.delete("/tasks/{task_id}")
def delete_list(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Tarea no encontrada"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Tarea eliminada correctamente"
    }
