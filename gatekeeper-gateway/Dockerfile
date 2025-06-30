FROM python:3.11
WORKDIR /app
COPY main.py .
COPY config.yaml .
COPY plugins ./plugins
COPY schemas ./schemas
COPY opa ./opa
RUN pip install fastapi[all] requests python-jose[cryptography] presidio-analyzer presidio-anonymizer
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
