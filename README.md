# Chotuve - Application Server
Grupo 11

--------------
## Pre Instrucciones

1. Instalar y configurar PostgreSQL
_... a documentar_

## Instrucciones: dos opciones

#### ~~Si se prefiere Docker~~ roto hasta nuevo aviso, usar virtualenv

1. Instalar [Docker Engine](https://docs.docker.com/engine/install/)


2. Buildear la imagen:
`docker build -t chotuve-appserver:latest .`

3. Correr el servidor:
`docker run -p 5000:5000 chotuve-appserver:latest`

4. Probar la REST API en `0.0.0.0:5000`

#### Si se prefiere Local OS con `virtualenv`


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

5. Ejecutar en debug mode
```
flask run
```

6. Probar la REST API en `0.0.0.0:5000`

---------------------------------------------


## API v0.1

Para ejecutar las requests, se recomienda utilizar [Postman](https://www.postman.com/downloads/)

- Obtener todos los videos guardados en la database:
`GET 0.0.0.0:5000/video`

- Obtener datos de un solo video:
`GET 0.0.0.0:5000/video/<id>`

- Obtener todos los comentarios de un video:
`GET 0.0.0.0:5000/video/<id>/comments`

- Postear un video:
`POST 0.0.0.0:5000/video`
con body:
```json
{
	
	"username": "nombre_usuario",
	"title":"titulo video",
    "description": "descripcion de ejemplo",
	"location":"lugar posteado"
	
}
```

- Postear un comentario:
`POST 0.0.0.0:5000/video/<id>/comments`
```json
{
	
	"author_user": "nombre_usuario",
	"text":"comentario de ejemplo"
	
}
```


_...a documentar_