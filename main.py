from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Mi gestor de tareas está funcionando 🚀"}