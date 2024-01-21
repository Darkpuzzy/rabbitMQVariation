FROM python:3.11.4-bullseye

ENV PYTHONUNBUFFERED=1

# Установка зависимостей LibreOffice
RUN apt-get update && apt-get install -y libreoffice

WORKDIR /code

COPY requirements.txt .

RUN pip3 install --no-cache-dir --upgrade --default-timeout=100  -r ./requirements.txt

COPY . /code

CMD ["python3", "consumer.py"]