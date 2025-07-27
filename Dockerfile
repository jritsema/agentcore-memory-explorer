FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*
COPY ./piplock.txt .
RUN pip3 install -r piplock.txt
COPY . .
ENTRYPOINT ["python", "-u", "main.py"]

