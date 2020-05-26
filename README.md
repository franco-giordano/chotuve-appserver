# Chotuve - Application Server
![Grupo](https://img.shields.io/badge/grupo-11-blue) [![Build Status](https://travis-ci.com/Franco-Giordano/chotuve-appserver.svg?token=7zpnJJggDS7tTpxSzkvp&branch=master)](https://travis-ci.com/Franco-Giordano/chotuve-appserver)
![api](https://img.shields.io/badge/api-v0.2-blueviolet)
[![sv](https://img.shields.io/badge/view-media%20sv-important)](https://github.com/sebalogue/chotuve-mediaserver)
[![sv](https://img.shields.io/badge/view-auth%20sv-important)](https://github.com/santiagomariani/chotube-auth-server)
[![sv](https://img.shields.io/badge/view-android-important)](https://github.com/javier2409/Chotuve-Android)

## Instrucciones

1. Instalar [Docker Engine](https://docs.docker.com/engine/install/) y [Docker Compose](https://docs.docker.com/compose/install/)

2. Levantar server + database
```docker-compose up```

4. Probar la REST API en `0.0.0.0:5000`



---------------------------------------------


## API v0.2

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
	"firebase-url":"...firebase.com..."
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
	
	"likes-video":true
	
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
	"fullname":"Cosme Fulanito",
	"email":"cosme_rivercampeon@gmail.com",
	"login-method":"facebook"
}
```

_login-method DEBE ser alguno de los tres: "email", "facebook" o "google"_

#### Login/Logout

- Logearse (solo verifica el token):
```POST 0.0.0.0:5000/auth```

- Cerrar sesion (no hace **absolutamente** nada):
```DELETE 0.0.0.0:5000/auth```

#### Amistades

- Ver amigos de un usuario [WIP]:
```GET 0.0.0.0:5000/users/<uuid>/friends```

- Enviar solicitud de amistad [NO IMPLEMENTADO]:
```POST 0.0.0.0:5000/users/<otheruuid>/friends```


- Ver solicitudes pendientes [NO IMPLEMENTADO]:
```GET 0.0.0.0:5000/users/<myuuid>/friends/requests```


- Aceptar/Rechazar solicitud pendient [NO IMPLEMENTADO]:
```GET 0.0.0.0:5000/users/<myuuid>/friends/requests/<otheruuid>```