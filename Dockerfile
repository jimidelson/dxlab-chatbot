FROM python:3.9-slim

WORKDIR /app
COPY app /app
COPY data /data

RUN pip install -r /app/requirements.txt

EXPOSE 5000

CMD ["python", "/app/app.py"]

