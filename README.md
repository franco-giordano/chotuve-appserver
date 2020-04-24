# Chotuve - Application Server


### Requisitos para el desarrollo
- [Docker Engine](https://docs.docker.com/engine/install/)

### Instrucciones

1. Buildear la imagen:
`docker build -t chotuve-appserver:latest .`

2. Correr el servidor:
`docker run -p 5000:5000 chotuve-appserver:latest`

3. Probar la REST API en `0.0.0.0:5000`

### API

- Obtener videos guardados en la database:
`GET en 0.0.0.0:5000/video`

_...a documentar_