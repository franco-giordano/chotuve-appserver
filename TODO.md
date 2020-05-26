# Tablas:
- amigos
- solicitudes amistad
- stats (???)
- chats (lo puede hacer firebase)

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

##### Login
POST /auth

##### Logout
DELETE /auth 

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
POST /users/$myid$/friends/requests/$req-id$

##### Recuperar password
POST /users/RECOVER_ENDPOINT_NAME

##### Escribir nueva password
POST /users/NEWPW_ENDPOINT_NAME