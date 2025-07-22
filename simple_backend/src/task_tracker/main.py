import json
from fastapi import FastAPI
from pydantic import BaseModel

class Task(BaseModel):
    id: int
    title:str
    status: str

class TaskFileStorage:
    def __init__(self, filepath: str):
        self.filepath = filepath
    
    def read(self):
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Task(**item) for item in data]
    
    def write(self, tasks):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([task.model_dump() for task in tasks], f, indent=2)

app = FastAPI()
storage = TaskFileStorage("tasks.json")

@app.get("/tasks")
def get_tasks():
    return storage.read()

@app.post("/tasks")
def create_task(task: Task):
    tasks = storage.read()
    tasks.append(task)
    storage.write(tasks)
    return task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, update_task: Task):
    tasks = storage.read()
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks[i] = update_task
            storage.write(tasks)
            return update_task
    return {"error": "Task not found"}
        

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    tasks = storage.read()
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(i)
            storage.write(tasks)
            return {"message": "Task deleted"}
    return {"error": "Task not found"}

