# base image with python 3
FROM python:3.8.1-slim-buster
WORKDIR /app

RUN apt-get update && apt-get install -y git

COPY . .

RUN pip install -r requirements.txt

# flask envs
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV APP_SETTINGS=production
ENV CH_MEDIASV_URL=http://chotuve-media-server.herokuapp.com:80
ENV CH_MEDIASV_TOKEN=CAMBIARESTO
ENV CH_AUTHSV_URL=http://chotuve-auth-server-10.herokuapp.com:80
ENV CH_AUTHSV_TOKEN=CAMBIARESTO

ENTRYPOINT ["sh", "/app/docker-entrypoint-prod.sh"]