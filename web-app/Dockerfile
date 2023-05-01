FROM python:3.9-slim

RUN apt-get update && apt-get install -y python3-pip

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip3 install -r requirements.txt && rm -rf /root/.cache/pip

COPY app /app/

CMD ["python", "main.py"]
