"""The module contains unit tests for API endpoints with both positive and negative testing scenarios."""

from bson import ObjectId
from fastapi.testclient import TestClient
from .main import app


def test_rood_pass():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to the app. Add '/docs' to your url to see the UI."}


def test_test_func_pass():
    with TestClient(app) as client:
        response = client.get("/api/test")
        assert response.status_code == 200
        assert response.json() == {"message": "The app is running smoothly."}


def test_create_task_pass():
    with TestClient(app) as client:
        task = {"title": "Test Task str", "description": "Some description", "status": "completed"}
        response = client.post("/api/tasks", json=task)
        assert response.status_code == 201
        inserted_task = app.database["tasks"].find_one({"_id": ObjectId(response.json()["id"])})
        assert inserted_task is not None
        assert inserted_task["title"] == "Test Task str"
        assert inserted_task["description"] == "Some description"
        assert inserted_task["status"] is True
        client.app.database["tasks"].delete_one({"_id": ObjectId(response.json()['id'])})

        task = {"title": "Test Task bool", "description": "Some description", "status": "false"}
        response = client.post("/api/tasks", json=task)
        assert response.status_code == 201
        inserted_task = app.database["tasks"].find_one({"_id": ObjectId(response.json()["id"])})
        assert inserted_task is not None
        assert inserted_task["title"] == "Test Task bool"
        assert inserted_task["description"] == "Some description"
        assert inserted_task["status"] is False
        client.app.database["tasks"].delete_one({"_id": ObjectId(response.json()['id'])})


def test_create_task_no_title_fail():
    with TestClient(app) as client:
        task = {"description": "Some description", "status": "completed"}
        response = client.post("/api/tasks", json=task)
        assert response.status_code == 422
        assert "The title is required" in response.json()["detail"][0].values()


def test_create_task_wrong_status_fail():
    with TestClient(app) as client:
        task = {"title": "Test Task", "description": "Some description", "status": "x"}
        response = client.post("/api/tasks", json=task)
        assert response.status_code == 422
        assert "Invalid status value. Write 'yes' or 'no', please." in response.json()["detail"][0].values()


def test_list_tasks_pass():
    with TestClient(app) as client:
        task = {"title": "Test Task", "description": "Some description", "status": "completed"}
        response = client.post("/api/tasks", json=task)
        inserted_task = app.database["tasks"].find_one({"_id": ObjectId(response.json()["id"])})

        response = client.get("/api/tasks")
        assert response.status_code == 200
        assert inserted_task in app.database["tasks"].find(limit=50)
        client.app.database["tasks"].delete_one(inserted_task)


def test_find_task_pass():
    with TestClient(app) as client:
        task = {"title": "Test Task", "description": "Some description", "status": "completed"}
        response = client.post("/api/tasks", json=task)
        inserted_task_id = response.json()["id"]

        response = client.get(f"/api/tasks/{inserted_task_id}")
        assert response.json()["title"] == "Test Task"
        assert response.json()["description"] == "Some description"
        assert response.json()["status"] == "completed"
        client.app.database["tasks"].delete_one({"_id": inserted_task_id})


def test_find_task_not_valid_id_fail():
    with TestClient(app) as client:
        response = client.get(f"/api/tasks/777")
        assert response.status_code == 404
        assert "The id 777 is not valid. " \
               "Please provide a valid ObjectId string." in response.json()["detail"]


def test_find_task_not_found_fail():
    with TestClient(app) as client:
        response = client.get(f"/api/tasks/644baa8eeaa2fd8cf8519216")
        assert response.status_code == 404
        assert "The task with id 644baa8eeaa2fd8cf8519216 " \
               "cannot be found!" in response.json()["detail"]


def test_update_task_pass():
    with TestClient(app) as client:
        task = {"title": "Test Task", "description": "Some description", "status": "completed"}
        response = client.post("/api/tasks", json=task)
        inserted_task_id = response.json()["id"]

        task_update = {"description": "Another description"}
        response = client.patch(f"/api/tasks/{inserted_task_id}", json=task_update)
        assert response.json()["id"] == inserted_task_id
        assert response.json()["description"] == "Another description"
        client.app.database["tasks"].delete_one({"_id": inserted_task_id})


def test_update_task_not_valid_id_fail():
    with TestClient(app) as client:
        response = client.patch(f"/api/tasks/777", json={})
        assert response.status_code == 404
        assert "The id 777 is not valid. " \
               "Please provide a valid ObjectId string." in response.json()["detail"]


def test_update_task_not_found_fail():
    with TestClient(app) as client:
        response = client.patch(f"/api/tasks/644baa8eeaa2fd8cf8519216", json={})
        assert response.status_code == 404
        assert "The task with id 644baa8eeaa2fd8cf8519216 " \
               "cannot be found!" in response.json()["detail"]


def test_delete_task_pass():
    with TestClient(app) as client:
        task = {"title": "Test Task", "description": "Some description", "status": "completed"}
        response = client.post("/api/tasks", json=task)
        inserted_task_id = response.json()["id"]
        response = client.delete(f"/api/tasks/{inserted_task_id}")
        assert response.status_code == 204


def test_delete_task_not_valid_id_fail():
    with TestClient(app) as client:
        response = client.delete(f"/api/tasks/777")
        assert response.status_code == 404
        assert "The id 777 is not valid. " \
               "Please provide a valid ObjectId string." in response.json()["detail"]


def test_delete_task_not_found_fail():
    with TestClient(app) as client:
        response = client.delete(f"/api/tasks/644baa8eeaa2fd8cf8519216")
        assert response.status_code == 404
        assert "The task with id 644baa8eeaa2fd8cf8519216 " \
               "cannot be found!" in response.json()["detail"]
