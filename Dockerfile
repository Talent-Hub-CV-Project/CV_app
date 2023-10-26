FROM python:3.10-slim

WORKDIR "/src"
COPY requirements/requirements.txt .
RUN pip install -r requirements.txt
RUN apt update && apt install ffmpeg libsm6 libxext6 -y
COPY . /
ENV PYTHONPATH=../
#RUN ["python", "main.py"]
