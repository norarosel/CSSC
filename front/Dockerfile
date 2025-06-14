FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/main.py main.py

ADD images images

ADD src src

CMD ["solara", "run", "src/main.py", "--host=0.0.0.0"]