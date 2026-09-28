FROM python:3.8-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    ffmpeg \
    pip \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt . 

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . . 

CMD ["python3", "flaskr/app.py"]
