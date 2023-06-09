﻿# To-Do List Application

A To-Do List application built with FastAPI and MongoDB.


## Endpoints

### Use the application via FastAPI Swagger UI

```
https://localhost:8000/docs
```

### Or use it via Postman

1. (GET) the list of tasks:
```
https://localhost:8000/api/tasks
```

2. (GET) details of the specific task:
```
https://localhost:8000/api/tasks/<task id>
```

3. (POST) a new task:
```
https://localhost:8000/api/tasks
```

4. (PATCH) an existing task:
```
https://localhost:8000/api/tasks/<task id>
```

5. (DELETE) an existing task:
```
https://localhost:8000/api/tasks/<task id>
```


## Setup of the project (without Docker)


#### Create and activate a virtual environment on Windows

- `python -m venv venv`
- `venv\Scripts\activate`


#### Create and activate a virtual environment on Linux

- `python3 -m venv venv && source venv/bin/activate`


#### Install dependencies

- `pip install --upgrade pip`
- `pip install -r requirements.txt`


#### Run the server

- `python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload`

The application is accessible on `http://127.0.0.1:8000/` or `http://localhost:8000/`.


## Setup of the project using Docker
(see Makefile for additional information)


#### Create and activate a virtual environment

- `python3 -m venv venv && source venv/bin/activate`


#### Create an image and start a container

- `make build`
or
- `docker-compose up -d  --build`


#### To stop the container

- `make stop`
or
- `docker-compose down`


#### To destroy ALL unused docker containers and images

- `make purge`
or
- `docker system prune -a`


## To run the tests (via PyTest lib)
- `pytest`
