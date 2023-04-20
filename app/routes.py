from typing import List
from fastapi import Request, Response, HTTPException, APIRouter, status
from fastapi.encoders import jsonable_encoder

from models import Task, TaskUpdate

router = APIRouter()


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED,
             response_description="The new task was added!")
def create_task(request: Request, task: Task):
    task = jsonable_encoder(task)
    new_task = request.app.database["tasks"].insert_one(task)
    created_task = request.app.database["tasks"].find_one(
        {"_id": new_task.inserted_id}
    )

    return created_task


@router.get("/", response_model=List[Task], status_code=status.HTTP_200_OK,
            response_description="The list of all tasks.")
def list_tasks(request: Request):
    tasks = list(request.app.database["tasks"].find(limit=50))
    return tasks


@router.get("/{id}", response_model=Task, status_code=status.HTTP_200_OK,
            response_description="Details of the specific task.")
def find_task(request: Request, task_id):
    task = request.app.database["tasks"].find_one({"_id": task_id})
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The task with id {task_id} cannot be found!")
    return task


@router.patch("/{id}", response_model=Task, status_code=status.HTTP_200_OK,
              response_description="Details of the specific task.")
def update_task(task_id, request: Request, task: TaskUpdate):
    modified_task = request.app.database["tasks"].find_one({"_id": task_id})
    if not modified_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The task with id {task_id} cannot be found!")

    update_request = task.dict(exclude_unset=True)
    if update_request:
        modified_task = request.app.database["tasks"].update_one({"_id": task_id, "$set": update_request})

    return modified_task


@router.delete("/{id}", response_description="Delete specific task")
def delete_task(task_id, request: Request, response: Response):
    deleted_task = request.app.database["tasks"].delete_one({"_id": task_id})
    if deleted_task.deleted_count:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"The task with id {task_id} cannot be found!")


