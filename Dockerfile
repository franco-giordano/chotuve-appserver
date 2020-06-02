# base image with python 3
FROM python:3.8.1-slim-buster
WORKDIR /app

RUN apt-get update && apt-get install -y git

COPY . .

RUN pip install -r requirements.txt

# flask envs
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

ENTRYPOINT ["sh", "/app/docker-entrypoint-prod.sh"]