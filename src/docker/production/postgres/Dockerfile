
FROM postgres:15-bullseye

# this is done for self-hosting database and backups
COPY ./docker/production/postgres/maintenance /usr/production/bin/maintenance

RUN chmod +x /usr/production/bin/maintenance/* 

RUN mv /usr/production/bin/maintenance/* /usr/production/bin && \
        rmdir /usr/production/bin/maintenance

# to create custom db user 
COPY ./docker/production/postgres/init-user-db.sh /docker-entrypoint-initdb.d/init-user-db.sh

RUN sed -i 's/\r$//g' /docker-entrypoint-initdb.d/init-user-db.sh

RUN chmod +x /docker-entrypoint-initdb.d/init-user-db.sh

