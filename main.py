from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
import json
import os
import shutil

app = FastAPI(title="To-Do List API")

# --- Middleware CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Plantilles ---
templates = Jinja2Templates(directory="templates")

# --- Model ---
class Task(BaseModel):
    title: str
    deadline: Optional[date] = None
    completed: bool = False

# --- Persistència en JSON ---
DB_FILE = "tasks.json"

def load_tasks() -> List[Task]:
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Task(**t) for t in data]
    except (json.JSONDecodeError, FileNotFoundError):
        backup = DB_FILE + ".bak"
        shutil.move(DB_FILE, backup)
        print(f"[WARN] Fitxer JSON corrupte. S’ha mogut a {backup}")
        return []

def save_tasks(tasks: List[Task]):
    tmp_file = DB_FILE + ".tmp"
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(jsonable_encoder(tasks), f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_file, DB_FILE)

# Carregar tasques inicials
tasks: List[Task] = load_tasks()

# --- Endpoints REST ---
@app.post("/tasks", response_model=Task)
def add_task(task: Task):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="El títol és obligatori")
    for t in tasks:
        if t.title == task.title and t.deadline == task.deadline:
            raise HTTPException(status_code=400, detail="Aquesta tasca ja existeix")
    tasks.append(task)
    save_tasks(tasks)
    return task

@app.get("/tasks", response_model=List[Task])
def list_tasks(completed: Optional[bool] = None):
    if completed is None:
        return tasks
    return [t for t in tasks if t.completed == completed]

@app.put("/tasks/{title}/complete", response_model=Task)
def complete_task(title: str):
    for t in tasks:
        if t.title == title:
            t.completed = True
            save_tasks(tasks)
            return t
    raise HTTPException(status_code=404, detail="Tasca no trobada")

@app.put("/tasks/{title}/uncomplete", response_model=Task)
def uncomplete_task(title: str):
    for t in tasks:
        if t.title == title:
            t.completed = False
            save_tasks(tasks)
            return t
    raise HTTPException(status_code=404, detail="Tasca no trobada")

@app.get("/tasks/completed", response_model=List[Task])
def get_completed_tasks():
    return [t for t in tasks if t.completed]

@app.get("/tasks/pending", response_model=List[Task])
def get_pending_tasks():
    return [t for t in tasks if not t.completed]

# --- Servir interfície web ---
@app.get("/", response_class=HTMLResponse)
def serve_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
