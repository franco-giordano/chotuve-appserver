# Chotuve - Application Server
![Grupo](https://img.shields.io/badge/grupo-11-blue)
[![Build Status](https://travis-ci.com/Franco-Giordano/chotuve-appserver.svg?token=7zpnJJggDS7tTpxSzkvp&branch=master)](https://travis-ci.com/Franco-Giordano/chotuve-appserver)
[![Coverage Status](https://coveralls.io/repos/github/Franco-Giordano/chotuve-appserver/badge.svg?branch=development&t=hXdO0j)](https://coveralls.io/github/Franco-Giordano/chotuve-appserver?branch=development)
![api](https://img.shields.io/badge/api-v0.3-blueviolet)
[![sv](https://img.shields.io/badge/view-media%20sv-important)](https://github.com/sebalogue/chotuve-mediaserver)
[![sv](https://img.shields.io/badge/view-auth%20sv-important)](https://github.com/santiagomariani/chotube-auth-server)
[![sv](https://img.shields.io/badge/view-android-important)](https://github.com/javier2409/Chotuve-Android)


## Instrucciones

1. Instalar [Docker Engine](https://docs.docker.com/engine/install/) y [Docker Compose](https://docs.docker.com/compose/install/)

2. Levantar server + database
```docker-compose up```

4. Probar la REST API en `0.0.0.0:5000`



---------------------------------------------


## API v0.3

Para ejecutar las requests, se recomienda utilizar [Postman](https://www.postman.com/downloads/)

**Salvo por registrarse o loguearse, TODOS los endpoints REQUIEREN el campo "x-access-token" en los headers, con un token valido**

#### Videos

- Obtener todos los videos guardados en la database:
`GET 0.0.0.0:5000/videos`

- Obtener datos de un solo video (sin comentarios):
`GET 0.0.0.0:5000/videos/<id>`

- Obtener todos los comentarios de un video:
`GET 0.0.0.0:5000/videos/<id>/comments`

- Postear un video:
`POST 0.0.0.0:5000/videos` con body:
```json
{
	
	"title":"titulo video",
	"description": "descripcion de ejemplo",
	"location":"lugar posteado",
	"firebase_url":"...firebase.com..."
}
```

- Postear un comentario:
`POST 0.0.0.0:5000/videos/<id>/comments` con body:
```json
{
	
	"text":"comentario de ejemplo"
	
}
```

- Obtener todas las reacciones a un video (username + like/dislike):
`GET 0.0.0.0:5000/videos/<id>/reactions` (en la respuesta: likes_video es true si es like, false si es dislike)


- Reaccionar a un video:
`POST 0.0.0.0:5000/videos/<id>/reactions` con body (true es like, false es dislike):
```json
{
	
	"likes_video":true
	
}
```

#### Usuarios

- Obtener datos publicos de un usuario
```GET 0.0.0.0:5000/users/<uuid>```

- Buscar usuarios con datos coincidentes [NO IMPLEMENTADO]:
```GET 0.0.0.0:5000/users?q=<name>```

- Obtener videos subidos por un usuario
```GET 0.0.0.0:5000/users/<uuid>/videos```

- Registrar un nuevo usuario:
```POST 0.0.0.0:5000/users```
con body:
```json
{
	"display_name":"Cosme Fulanito",
	"email":"cosme_rivercampeon@gmail.com",
	"image_location":"https://image.freepik.com/foto-gratis/playa-tropical_74190-188.jpg",
	"phone_number":"+542323232323"
}
```

- Modificar datos de un usuario:
`PUT 0.0.0.0:4000/users/<id>` con body (pueden enviarse solo los datos que cambian):
```json
{
	
	"email": "juanperez@gmail.com",
	"display_name":"Matias Perez",
	"phone_number": "+5492264511422",
	"image_location":"https://image.freepik.com/foto-gratis/playa-tropical_74190-188.jpg"
	
}
```
#### Amistades

- Ver amigos de un usuario:
```GET 0.0.0.0:5000/users/<uuid>/friends```

- Enviar solicitud de amistad:
```POST 0.0.0.0:5000/users/<otheruuid>/friends/requests``` sin body (obtiene el id de quien envia desde el token)


- Ver mis solicitudes pendientes:
```GET 0.0.0.0:5000/users/<myuuid>/friends/requests```


- Aceptar/Rechazar solicitud pendiente:
```POST 0.0.0.0:5000/users/<myuuid>/friends/requests/<otheruuid>``` con body
```json
{
	"accept":true
}
```
(accept true para aceptar, accept false para rechazar)
