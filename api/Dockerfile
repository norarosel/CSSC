FROM python:3.11

WORKDIR /api

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

# Copy app source code folder
ADD app app

# Run uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--root-path", "/api", "--log-config", "/api/app/config/logging.yaml"]