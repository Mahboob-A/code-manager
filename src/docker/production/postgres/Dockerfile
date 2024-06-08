
FROM postgres:15-bullseye

# this is done for self-hosting database and backups
COPY ./docker/dev/postgres/maintenance /usr/local/bin/maintenance

RUN chmod +x /usr/local/bin/maintenance/* 

RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
        && rmdir /usr/local/bin/maintenance

# to create custom db user 
COPY ./docker/dev/postgres/init-user-db.sh /docker-entrypoint-initdb.d/init-user-db.sh

RUN sed -i 's/\r$//g' /docker-entrypoint-initdb.d/init-user-db.sh

RUN chmod +x /docker-entrypoint-initdb.d/init-user-db.sh

