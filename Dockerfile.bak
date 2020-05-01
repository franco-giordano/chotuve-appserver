# Retrieving Alpine Docker image template for Python
FROM python:3.6-alpine

# Installing Python 3, Pip and Postgres
RUN apk update
RUN apk --no-cache add python3-dev
RUN pip3 install --upgrade pip
RUN apk add --no-cache postgresql postgresql-contrib postgresql-dev gcc musl-dev
RUN pip3 install psycopg2

# Creating Docker's working directory
WORKDIR /app

# Copying source code to the Docker's working directory
COPY ./requirements.txt /app

# Installing Python modules
RUN pip3 --no-cache-dir install -Ur requirements.txt

COPY . .

# Exposing Docker port
EXPOSE 5000

RUN source .env

CMD ["sh", "-c", "flask run -h 0.0.0.0 -p 5000"]