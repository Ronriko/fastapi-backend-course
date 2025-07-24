import os
from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv
from base import BaseHTTPClient
from llm import LLMClient
import requests

load_dotenv()

BASE_URL = os.getenv("MOCKAPI_BASE_URL") + "/tasks"
llm = LLMClient()
router = APIRouter()


class TasksClient(BaseHTTPClient):
    def parse(self, response: requests.Response):
        return response.json()


tasks_api = TasksClient(BASE_URL)


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
    return TaskListResponse(tasks=tasks_api.request("get", ""))


@router.post("/tasks", response_model=Task)
def create_task(task: Task):
    solution = llm.generate_solution(task.title)
    task.title += f"Решение от ИИ: \n{solution}"
    return tasks_api.request(
        "post", "", json=task.model_dump(exclude={"id"}, exclude_unset=True)
    )


@router.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, update_task: Task):
    return tasks_api.request(
        "put", task_id, json=update_task.model_dump(exclude={"id"}, exclude_unset=True)
    )


@router.delete("/tasks/{task_id}", response_model=MessageResponse)
def delete_task(task_id: str):
    tasks_api.request("delete", task_id)
    return MessageResponse(message="Task deleted")
