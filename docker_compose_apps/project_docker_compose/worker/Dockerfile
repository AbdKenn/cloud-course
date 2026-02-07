FROM python:3.11-slim
WORKDIR /worker
RUN pip install redis
COPY worker.py .
CMD ["python", "worker.py"]
