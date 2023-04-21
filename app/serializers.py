def task_serializer(task):
    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "description": task["description"],
        "status": task["status"]
    }


def list_of_tasks_serializer(tasks):
    return [task_serializer(task) for task in tasks]
