from typing import List

import bson
from fastapi import Request, Response, HTTPException, APIRouter, status
from fastapi.encoders import jsonable_encoder
from serializers import task_serializer, list_of_tasks_serializer
from models import Task, TaskUpdate, TaskDetails
from bson import ObjectId

router = APIRouter()


@router.post("/", response_model=TaskDetails, status_code=status.HTTP_201_CREATED,
             response_description="The new task was added!")
def create_task(request: Request, task: Task):
    task = jsonable_encoder(task)
    new_task = request.app.database["tasks"].insert_one(task)
    created_task = request.app.database["tasks"].find_one(
        {"_id": new_task.inserted_id}
    )

    created_task["id"] = str(created_task["_id"])

    return TaskDetails(**created_task)


@router.get("/", response_model=List[TaskDetails], status_code=status.HTTP_200_OK,
            response_description="The list of all tasks.")
def list_tasks(request: Request):
    tasks = list_of_tasks_serializer(request.app.database["tasks"].find(limit=50))
    return tasks


@router.get("/{task_id}", response_model=TaskDetails, status_code=status.HTTP_200_OK,
            response_description="Details of the specific task.")
def find_task(request: Request, task_id: str):
    try:
        task_object_id = ObjectId(task_id)
    except bson.errors.InvalidId:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The id {task_id} is not valid. Please provide a valid ObjectId string.")
    else:
        task = request.app.database["tasks"].find_one({"_id": task_object_id})
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The task with id {task_id} cannot be found!")
    return task_serializer(task)


@router.patch("/{task_id}", response_model=TaskDetails, status_code=status.HTTP_200_OK,
              response_description="Details of the specific task.")
def update_task(task_id, request: Request, task: TaskUpdate):
    try:
        task_object_id = ObjectId(task_id)
    except bson.errors.InvalidId:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The id {task_id} is not valid. Please provide a valid ObjectId string.")
    else:
        modified_task = request.app.database["tasks"].find_one({"_id": task_object_id})
    if not modified_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The task with id {task_id} cannot be found!")

    update_request = task.dict(exclude_unset=True)
    if update_request:
        request.app.database["tasks"].update_one({"_id": task_object_id}, {"$set": update_request})
        modified_task = request.app.database["tasks"].find_one({"_id": task_object_id})

    return {"id": str(modified_task["_id"]), **modified_task}


@router.delete("/{task_id}", response_description="Delete specific task")
def delete_task(task_id, request: Request, response: Response):
    try:
        task_object_id = ObjectId(task_id)
    except bson.errors.InvalidId:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The id {task_id} is not valid. Please provide a valid ObjectId string.")
    else:
        deleted_task = request.app.database["tasks"].delete_one({"_id": task_object_id})
    if deleted_task.deleted_count:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"The task with id {task_id} cannot be found!")


