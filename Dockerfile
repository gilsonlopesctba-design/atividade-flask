FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=main

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]