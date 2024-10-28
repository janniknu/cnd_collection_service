FROM python:3.11-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED=1

WORKDIR /CloudNativeDevelopment

RUN pip install --upgrade pip
COPY  requirements.txt .
RUN pip install -r requirements.txt

COPY . .

#CMD python3 manage.py runserver 0.0.0.0:8000

