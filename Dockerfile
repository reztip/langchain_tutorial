FROM python:3.12.3-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./src/* .

CMD ["streamlit", "run", "main.py"]

