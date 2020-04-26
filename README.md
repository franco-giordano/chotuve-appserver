# Chotuve - Application Server
Grupo 11

--------------
## Pre Instrucciones

1. Instalar y [configurar PostgreSQL con este video](https://www.youtube.com/watch?v=-LwI4HMR_Eg)

2. Crear base de datos y migrarla
```
createdb chotuve-appserver-dev
createdb chotuve-appserver-prod

cd chotuve-appserver
python3 manage.py db init
python3 manage.py db migrate
python3 manage.py db upgrade
```

3. Reemplazar `franco_g` y `chotuve` por tu user y password de PostgreSQL en archivo .env:
```bash
...
export DATABASE_DEV_URL="...franco_g:chotuve..."
export DATABASE_PROD_URL="...franco_g:chotuve..."

```

## Instrucciones: dos opciones

#### Si se prefiere Docker (sin gunicorn ni live update)

1. Instalar [Docker Engine](https://docs.docker.com/engine/install/)

2. Buildear la imagen:
```
docker build -t chotuve-appserver:latest .
```

3. Correr el servidor:
```
docker run --net host -p 5000:5000 chotuve-appserver
```

4. Probar la REST API en `0.0.0.0:5000`

#### Si se prefiere Local OS con `virtualenv` (con gunicorn y live update)


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

5. Definir variables de entorno:
```
source .env
```


6. Ejecutar en debug mode
```
gunicorn -b 0.0.0.0:5000 --reload run:app
```

7. Probar la REST API en `0.0.0.0:5000`

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
	
	"comment_username": "nombre_usuario",
	"text":"comentario de ejemplo"
	
}
```


_...a documentar_
