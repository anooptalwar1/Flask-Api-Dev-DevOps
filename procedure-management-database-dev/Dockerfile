FROM mysql:latest as builder

# That file does the DB initialization but also runs mysql daemon, by removing the last line it will only init
RUN ["sed", "-i", "s/exec \"$@\"/echo \"not running $@\"/", "/usr/local/bin/docker-entrypoint.sh"]

# needed for intialization
ENV MYSQL_ROOT_PASSWORD=Passw0rd

ADD user_management_db.sql /var/lib/mysql
ADD procedure_management_db.sql /var/lib/mysql

COPY user_management_db.sql /docker-entrypoint-initdb.d/
COPY procedure_management_db.sql /docker-entrypoint-initdb.d/


RUN ["/usr/local/bin/docker-entrypoint.sh", "mysqld", "--datadir", "/initialized-db"]

FROM mysql:latest

COPY --from=builder /initialized-db /var/lib/mysql

EXPOSE 3306
