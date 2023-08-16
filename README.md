# ReservationsSystemAPI #

## Endpoints ##

### List of rooms ###

GET `/rooms`

Returns a list of rooms.


### Get a single room ###

GET `/room/:roomId`

Retrieve detailed information about a room.


### Add room ###

POST `/room`

Allows you to add room to list.

The request body needs to be in JSON format and include the following properties:

 - `name` - String - Required
 - `description` - String
 - `capacity` - Integer
 - `projector` - Boolean
 - `conditioning` - Boolean
 - `tv` - Boolean
 - `ethernet` - Boolean
 - `wifi` - Boolean
 - `whiteboard` - Boolean

Example:
```
POST /room/

{
   "name": "101",
   "description": "Sala konferencyjna 1",
   "capacity": 100,
   "projector": true,
   "conditioning": true,
   "tv": false,
   "ethernet": true,
   "wifi": true,
   "whiteboard": false
}
```


### Get all events ###

GET `/events`

Allows you to view all events.


### View an event ###

GET `/event/:eventId`

Allows you to view an existing event.


### All events for room on date ###

GET `/room/:roomId/events`

Allows you to view all events for room on given date.

Required query parameters:

- day: number of day
- month: number of month
- year: number of year

**Possible errors**

Status code 400 - Try changing the value of "roomId" parameter


### Nearest events for room ###

GET `/room/:roomId/events`

Allows you to view up to 20 nearest events for room.

Optional query parameters:

- limit: a number between 1 and 20.


### Add event ###

POST `/event`

Allows you to add event. 

If user token is provided, the ownerId will be assigned to user with given token, else ownerId will be 'undefined'.

The request body needs to be in JSON format and include the following properties:

 - `name` - String - Required
 - `description` - String
 - `link` - String
 - `begin` - DateTime - Required
 - `end` - DateTime - Required
 - `roomsId` - List of Integers

Example:
```
POST /event/

{
    "name": "Konferencja 1",
    "description": "Spotkanie z klientem",
    "link": null,
    "begin": "2023-08-10T09:00:00",
    "end": "2023-08-10T09:30:00",
    "roomsId": [1]
}
```

**Possible errors**

Status code 400 - Try changing the value of "begin" and "end" parameters.


### Registration ###

POST `/register`

Allows you to register new user. Returns JWT token.

The request body needs to be in JSON format and include the following properties:

 - `email` - String - Required
 - `firstName` - String - Required
 - `lastName` - String - Required
 - `password` - String - Required - cannot be shorter than 6 characters

Example:
```
POST /register/

{
    "email": "test@test.com",
    "firstName": "test",
    "lastName": "test",
    "password": "test123"
}
```

**Possible errors**

Status code 400 - Try changing the value of "email" parameter.

### Login ###

POST `/login`

Allows you to login as existing user. Returns JWT token.

The request body needs to be in JSON format and include the following properties:

 - `email` - String - Required
 - `password` - String - Required

Example:
```
POST /login/

{
    "email": "test@test.com",
    "password": "test123"
}
```

**Possible errors**

Status code 400 - Try changing the value of "email" or "password" parameter.

### Get currently logged user ###

GET `/current_user`

Returns user by provided token.

The request header needs to contain JWT token.

Example
```
{
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.e30.B1iOFeMevN3u74w5EuMSZWEIBkEy502nj6u8zYywf1s"
}
```

**Possible errors**

Status code 400 - Try using token of already registered user.
