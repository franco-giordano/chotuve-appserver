# Endpoints

### Videos
GET POST /videos
GET /videos/$id$
GET POST /videos/$id$/comments
GET POST /videos/$id$/reactions

### Users
GET /users/$id$
GET /users/$id$/videos
GET /users?q=$query$

##### Registro
POST /users

##### Cambiar datos personales
PUT /users/$myid$

### Amistades
##### Ver amigos
GET /users/$id$/friends

##### Enviar solicitud
POST /users/$otherid$/friends

##### Ver todas mis solicitudes pendientes
GET /users/$myid$/friends/requests

##### Aceptar/Declinar solicitud
POST /users/$myid$/friends/requests/$otherid$

##### TODO Recuperar password
POST /users/RECOVER_ENDPOINT_NAME

##### TODO Escribir nueva password 
POST /users/NEWPW_ENDPOINT_NAME


# ALL TODOs:
- Resetear contrasenia
- stats
- chatting
- modificar metadata videos
- modificar comentarios
- modificar reaccion
- borrar video
- borrar comentario
- borrar reaccion
- buscar usuario (/users?name=...)
- sugerir videos segun motor de reglas
- pylint
- Manuales:
    - Manual de administrador: Instalación y configuración
    - Definición de Arquitectura / Diseño de la aplicación (Debe incluir especificación de Api REST: OpenAPI 2.0)
