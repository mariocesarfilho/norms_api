FROM python:3.12-slim

WORKDIR /app

# Copiar as dependências antes do código preserva esta camada do cache quando
# apenas os arquivos da aplicação mudam.
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
