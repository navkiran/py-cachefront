FROM mysql:8

ENV MYSQL_DATABASE mydb
ENV MYSQL_ROOT_PASSWORD secret
COPY init.sql /docker-entrypoint-initdb.d/
COPY my.cnf /etc/mysql/conf.d/