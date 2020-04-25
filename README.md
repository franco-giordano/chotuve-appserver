# Chotuve - Application Server


### Requisitos para el desarrollo
- [Docker Engine](https://docs.docker.com/engine/install/)

### Instrucciones

#### Docker

1. Buildear la imagen:
`docker build -t chotuve-appserver:latest .`

2. Correr el servidor:
`docker run -p 5000:5000 chotuve-appserver:latest`

3. Probar la REST API en `0.0.0.0:5000`

#### Local OS con `virtualenv`


1. Instalar herramienta virtualenv
```
pip3 install virtualenv
```

2. Crear un virtualenv en la carpeta del proyecto
```
cd chotuve-appserver
virtualenv -p python3 venv
```

3. Activarlo
```
source venv/bin/activate
```

4. Ya activado el venv, instalamos dependencias
```
pip install -Ur requirements.txt
```

5. Ejecutar
```
gunicorn wsgi --log-file -
```

6. Probar la REST API en `0.0.0.0:5000`




### API

- Obtener videos guardados en la database:
`GET en 0.0.0.0:5000/video`

_...a documentar_