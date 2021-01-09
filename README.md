# Social network

This is a test social-network task.

This application consists of two services: social-network and auth-service.
The purpose of the first is to store posts and to implement endpoints to work
with them. Social-network service uses auth-service to get the information
about user authentication and other stuff for providing security.

## Preparing to run
First you need to create **.envs** files. In folders with applications
you can see **.envs.example** files, they need to be copied and renamed,
the variables in these files must be redefined from example values to 
real values.

Run this lines in terminal to implement the instructions from above:
```shell
cd test-task
cp social-network/.envs.example social-network/.envs
cp auth-service/.envs.example auth-service/.envs
cp automated-bot/.envs.example automated-bot/.envs
```

After you've done that, you should redefine the variables.
I afford you the following values.

##### For auth-service:
- SECRET_KEY=_auth-secret-key_
- POSTGRES_DB=_db-auth_
- POSTGRES_HOST=_db-auth_
- POSTGRES_PORT=_5432_

| ⚠WARNING: POSTGRES_HOST must be similar as auth database service in docker-compose. If you want to make changes, be sure of what you are doing.|
| --- |

##### For social-network:
- SECRET_KEY=_social-network-secret-key_
- AUTH_SERVICE_URL=_http://auth-service:8010/_
- WEB_SERVICE_JWT - _we'll deal with it later_
- POSTGRES_DB=_db-social-network_
- POSTGRES_HOST=_db-social-network_
- POSTGRES_PORT=_5432_

| ⚠WARNING: POSTGRES_HOST must be similar as auth database service in docker-compose. AUTH_SERVICE_URL must contain auth service name from docker-compose. If you want to make changes, be sure of what you are doing.|
| --- |

##### For automated-bot:
- AUTH_SERVICE_API_URL=_http://auth-service:8010/api/_
- SOCIAL_NETWORK_SERVICE_API_URL=_http://social-network:8000/api/_

| ⚠WARNING: AUTH_SERVICE_API_URL and SOCIAL_NETWORK_SERVICE_API_URL must contain auth-service and social-network names from docker-compose. If you want to make changes, be sure of what you are doing.|
| --- |

Now, when the services are configured, we can run the application. The point
is that we have to do some more stuff to let our services to communicate with
each other. As auth-service uses JWT authentication, the social-network service
must have its own account with assigned JWT token, without this it would not
be able to send any request to the auth-service, that requires admin or user
privileges. So let's do it.

Run this command to start services:
```shell
make up
```

Let's create a user through signup endpoint. We need to do it using some
application, that lets us to send http requests. For these purposes I use
*Postman*, but let's use *curl* for now. 

Run this in your command line:
```shell
curl -XPOST -H "Content-type: application/json" -d '{
"username": "social-network-service",
"password": "S0mE-pa$$",
"first_name": "social-network",
"last_name": "service"
}' 'http://127.0.0.1:8010/api/signup/'
```

It will create a user. Now let's give to this user the staff status. It
is required because some endpoints require the user to be an admin.

Run this command to create a superuser in django admin:
```shell
make run-auth command=createsuperuser
```

After the user is created, go to **http://127.0.0.1:8010/admin** and
authorize as the user you've just created. Find the user with username
**social-network-service** and make him staff.

Then let's gain a token for social-network-service. To do this, we need
simply login. To login as social-network-service, run the following command:
```shell
curl -XPOST -H "Content-type: application/json" -d '{
"username": "social-network-service",
"password": "S0mE-pa$$"
}' 'http://127.0.0.1:8010/api/login/'
```
It will return to you an access and a refresh tokens. Social-network-service
token will be valid for the next 7 days. If you want this term to be more
continuous, you need to do the next thing: go to https://jwt.io. Paste
an access token to the 'Encoded' field, then change 'exp' to the value
that you need (for example 3610000000). Next thing you need to do is
paste your auth-service **SECRET_KEY** instead of 'your-256-bit-secret'
on this site. After this, you will see an absolutely valid JWT token in
the 'Encoded' field. Now you can copy it and use for social-network service.

The next thing to do is pasting this JWT token to .envs of social-network.
To make changes be applied, drop your docker containers by running this:
```shell
make down
```
Then set the value of **WEB_SERVICE_JWT** in social-network/.envs to
the access JWT token value that you got in previous steps.

After that you can run the services again:
```shell
make up
```

That's all. Now the application is ready to accept connections.

## Available make commands
Run the application:
```shell
make up
```
Shutdown the application:
```shell
make down
```
Run a management command on the auth-service:
```shell
make run-auth command=<your_command>
```
Run a management command on the social-network:
```shell
make run-sn command=<your_command>
```
Run automated bot:
```shell
make run-bot
```

## Automated bot
This bot is able to create fake users, create posts and make likes on
these posts. After the application is configured and all servers are
ready to accept connections, you can run:
```shell
make run-bot
```

## API Endpoints
User signup:
```http request
POST http://127.0.0.1:8010/api/signup/
Content-Type: application/json
```
User login:
```http request
POST http://127.0.0.1:8010/api/login/
Content-Type: application/json
```
Post creation:
```http request
POST http://127.0.0.1:8000/api/posts/
Content-Type: application/json
Authorization: 'Bearer J8nf2834hfWJWUu382fH2jfjK.2hj8jh8f2j34Hfh8hwiOOUHFiher.j29f3jhf432hf'
```
Get all posts:
```http request
GET http://127.0.0.1:8000/api/posts/
Authorization: 'Bearer J8nf2834hfWJWUu382fH2jfjK.2hj8jh8f2j34Hfh8hwiOOUHFiher.j29f3jhf432hf'
```
Read single post:
```http request
GET http://127.0.0.1:8000/api/posts/{post_id}
Authorization: 'Bearer J8nf2834hfWJWUu382fH2jfjK.2hj8jh8f2j34Hfh8hwiOOUHFiher.j29f3jhf432hf'
```
Post like:
```http request
POST http://127.0.0.1:8000/api/like-post/
Content-Type: application/json
Authorization: 'Bearer J8nf2834hfWJWUu382fH2jfjK.2hj8jh8f2j34Hfh8hwiOOUHFiher.j29f3jhf432hf'
```
Get likes analytics for a period of time:
```http request
GET http://127.0.0.1:8000/api/likes-analytics/?date_from=2021-01-01&date_to=2021-03-03
Authorization: 'Bearer J8nf2834hfWJWUu382fH2jfjK.2hj8jh8f2j34Hfh8hwiOOUHFiher.j29f3jhf432hf'
```
Get user statistics (you must be staff):
```http request
POST http://127.0.0.1:8010/api/users-info/
Content-Type: application/json
Authorization: 'Bearer J8nf2834hfWJWUu382fH2jfjK.2hj8jh8f2j34Hfh8hwiOOUHFiher.j29f3jhf432hf'
```
