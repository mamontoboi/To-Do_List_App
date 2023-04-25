FROM python:3.11-alpine
EXPOSE 8000

WORKDIR /task_list_app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt  /task_list_app/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /task_list_app
