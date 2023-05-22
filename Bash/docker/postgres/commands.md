sources: https://hub.docker.com/_/postgres \
https://dev.to/stefanopassador/docker-compose-with-python-and-posgresql-33kk


### Setup
Up the container:
```shell
$ docker run --name postgres-container \
  -e POSTGRES_PASSWORD=password123 \
  -p 5432:5432 -d postgres:latest
```
the default db+user are named `postgres`, but if you want you can add
the environment variable:
```shell
  -e POSTGRES_USER=username \
  -e POSTGRES_DB=database \
```


#### Config new DB:
```shell
$ docker exec -it postgres-container bash
root# su postgres
postgres$ psql
postgres# $ CREATE USER username PASSWORD 'password' CREATEDB;
postgres# $ CREATE DATABASE notifications WITH ENCODING='UTF8' OWNER=username;
postgres# $ \connect notifications
notifications# $ GRANT ALL PRIVILEGES ON DATABASE notifications TO username;
notifications# $ GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO username;
notifications# $ GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO username;
```

### stop/ start the container
Stop the container:
```shell
$ docker stop postgres-container
```
Start again the container:
```shell
$ docker start postgres-container
```

### Uses
To see all databases/tables:
- ```postgres# $  \l```
- ```postgres# $  \dt```
- ```postgres# $  \connect {DB_NAME}```

