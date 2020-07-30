# Chotuve - Application Server
![Grupo](https://img.shields.io/badge/grupo-11-blue)
[![Build Status](https://travis-ci.com/Franco-Giordano/chotuve-appserver.svg?token=7zpnJJggDS7tTpxSzkvp&branch=staging)](https://travis-ci.com/Franco-Giordano/chotuve-appserver)
[![Coverage Status](https://coveralls.io/repos/github/Franco-Giordano/chotuve-appserver/badge.svg?branch=staging&t=hXdO0j)](https://coveralls.io/github/Franco-Giordano/chotuve-appserver?branch=staging)
![api](https://img.shields.io/badge/api-v1.1.2-blueviolet)
[![sv](https://img.shields.io/badge/view-media%20sv-important)](https://github.com/sebalogue/chotuve-mediaserver)
[![sv](https://img.shields.io/badge/view-auth%20sv-important)](https://github.com/santiagomariani/chotuve-auth-server)
[![sv](https://img.shields.io/badge/view-android-important)](https://github.com/javier2409/Chotuve-Android)
[![sv](https://img.shields.io/badge/view-web%20front-important)](https://github.com/santiagomariani/chotuve-web-front)



## Instrucciones

### Desarrollo

1. Instalar [Docker Engine](https://docs.docker.com/engine/install/) y [Docker Compose](https://docs.docker.com/compose/install/)

2. Levantar server + database: `docker-compose up --build`

4. Probar la REST API en `0.0.0.0:5000`. Utilizara los servidores de Staging para comunicaciones externas, URLs definidas en .env.dev

### Produccion

1. Instalar Docker Engine

2. Buildear la imagen: `docker build -t chotuve-appserver .`

3. Levantar la imagen: `docker run --env PORT=5000 -p 5000:5000 --name chotuve-appserver chotuve-appserver`. URLs definidas en Dockerfile

### Deploy

Para deployear, basta con pushear a master y Travis se encargara del resto. Para deployear a Staging es la misma idea: deployear a rama Staging. Utiliza las variables de entorno definidas en el mismo Heroku.



---------------------------------------------


## API

Ver archivo [OpenApi.yaml aqui](https://github.com/Franco-Giordano/chotuve-appserver/blob/master/OPENAPI.yaml)
