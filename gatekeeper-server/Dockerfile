FROM python:3.11
WORKDIR /app
COPY main.py .
RUN pip install fastapi[all]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
