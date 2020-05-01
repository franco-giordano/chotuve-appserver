# Chotuve - Application Server
![Grupo](https://img.shields.io/badge/grupo-11-blue) [![Build Status](https://travis-ci.com/Franco-Giordano/chotuve-appserver.svg?token=7zpnJJggDS7tTpxSzkvp&branch=master)](https://travis-ci.com/Franco-Giordano/chotuve-appserver)
![api](https://img.shields.io/badge/api-v0.1-blueviolet)
[![sv](https://img.shields.io/badge/view-media%20sv-important)](https://github.com/sebalogue/chotuve-mediaserver)
[![sv](https://img.shields.io/badge/view-auth%20sv-important)](https://github.com/santiagomariani/chotube-auth-server)
[![sv](https://img.shields.io/badge/view-android-important)](https://github.com/javier2409/Chotuve-Android)

## Instrucciones

1. Instalar [Docker Engine](https://docs.docker.com/engine/install/) y [Docker Compose](https://docs.docker.com/compose/install/)

2. Levantar server + database
```docker-compose up```

4. Probar la REST API en `0.0.0.0:5000`



---------------------------------------------


## API v0.1

Para ejecutar las requests, se recomienda utilizar [Postman](https://www.postman.com/downloads/)

- Obtener todos los videos guardados en la database:
`GET 0.0.0.0:5000/video`

- Obtener datos de un solo video (sin comentarios):
`GET 0.0.0.0:5000/video/<id>`

- Obtener todos los comentarios de un video:
`GET 0.0.0.0:5000/video/<id>/comments`

- Postear un video:
`POST 0.0.0.0:5000/video` con body:
```json
{
	
	"username": "nombre_usuario",
	"title":"titulo video",
	"description": "descripcion de ejemplo",
	"location":"lugar posteado"
	
}
```

- Postear un comentario:
`POST 0.0.0.0:5000/video/<id>/comments` con body:
```json
{
	
	"comment_username": "nombre_usuario",
	"text":"comentario de ejemplo"
	
}
```

- Obtener todas las reacciones a un video (username + like/dislike):
`GET 0.0.0.0:5000/video/<id>/reactions` (en la respuesta: likes_video es true si es like, false si es dislike)


- Reaccionar a un video:
`POST 0.0.0.0:5000/video/<id>/reactions` con body (true es like, false es dislike):
```json
{
	
	"username": "nombre_usuario",
	"likes_video":true
	
}
```
_si el usuario ya reacciono al video, se actualiza su reaccion, no se crea una nueva_

- Obtener videos subidos por un usuario
```GET 0.0.0.0:5000/user/<username>/videos```

