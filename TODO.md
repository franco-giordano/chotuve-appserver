# Tablas:
- amigos
- solicitudes amistad
- stats (???)
- chats (lo puede hacer firebase)

# Endpoints

### Videos
GET POST /video
GET /video/$id$
GET POST /video/$id$/comments
GET POST /video/$id$/reactions

### Users
GET /user/$id$
GET /user/$id$/videos
GET /user?q=$query$

##### Registro
POST /user

##### Login
POST /auth

##### Logout
DELETE /auth 

##### Cambiar datos personales
PUT /user/me (o $myid$?)

### Amistades
##### Enviar solicitud
POST /user/$otherid$/friends

##### Ver todas mis solicitudes pendientes
GET /user/$myid$/friends/requests

##### Aceptar/Declinar/Ver solicitud
GET /user/$myid$/friends/requests/$req-id$
POST /user/$myid$/friends/requests/$req-id$