FROM python:3.11

RUN apt update && apt install -y ffmpeg

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD gunicorn app:app --bind 0.0.0.0:$PORT