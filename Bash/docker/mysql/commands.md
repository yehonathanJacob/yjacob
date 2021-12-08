source:
https://medium.com/swlh/how-to-connect-to-mysql-docker-from-python-application-on-macos-mojave-32c7834e5afa

### Setup
Up the container:
```shell
$ docker run --name=user_mysql_1 \
  --env="MYSQL_ROOT_PASSWORD=root_password" \
  -p 3306:3306 -d mysql:latest
```

Config the db:
```shell
$ docker run --name=user_mysql_1 --env="MYSQL_ROOT_PASSWORD=root_password" -p 3306:3306 -d mysql:latest
mysql> CREATE DATABASE test_db;
mysql> use test_db;
mysql> CREATE TABLE test_table (userId INT NOT NULL AUTO_INCREMENT PRIMARY KEY, firstName VARCHAR(20), lastName VARCHAR(20));
mysql> CREATE USER 'newuser'@'%' IDENTIFIED BY 'newpassword';
mysql> GRANT ALL PRIVILEGES ON test_db.* to 'newuser'@'%';
```

