FROM python:3.11-slim

# Define working directory
WORKDIR /api

# Copia os arquivos necessários
COPY . /api

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/api

# Comando padrão: gunicorn com uvicorn workers
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]
