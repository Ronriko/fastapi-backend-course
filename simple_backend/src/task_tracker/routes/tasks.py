import os
import requests
from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv
from llm import LLMClient

load_dotenv()

BASE_URL = os.getenv("MOCKAPI_BASE_URL") + "/tasks"
llm = LLMClient()
router = APIRouter()


class Task(BaseModel):
    id: str | None = None
    title: str
    status: str


class TaskListResponse(BaseModel):
    tasks: list[Task]


class MessageResponse(BaseModel):
    message: str


@router.get("/tasks", response_model=TaskListResponse)
def get_tasks():
    response = requests.get(BASE_URL)
    response.raise_for_status()
    tasks = response.json()
    return TaskListResponse(tasks)


@router.post("/tasks", response_model=Task)
def create_task(task: Task):
    solution = llm.generate_solution(task.title)
    task.title += f"Решение от ИИ: \n{solution}"
    response = requests.post(
        BASE_URL, json=task.model_dump(exclude={"id"}, exclude_unset=True)
    )
    response.raise_for_status()
    tasks = response.json()
    return tasks


@router.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, update_task: Task):
    url = f"{BASE_URL}/{task_id}"
    response = requests.put(
        url, json=update_task.model_dump(exclude={"id"}, exclude_unset=True)
    )
    response.raise_for_status
    tasks = response.json()
    return tasks


@router.delete("/tasks/{task_id}", response_model=MessageResponse)
def delete_task(task_id: str):
    url = f"{BASE_URL}/{task_id}"
    response = requests.delete(url)
    response.raise_for_status
    return {"message": "Task deleted"}
