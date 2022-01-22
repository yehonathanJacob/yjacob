FROM python:3.7

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install opencv-python
RUN pip install mediapipe

COPY . /app