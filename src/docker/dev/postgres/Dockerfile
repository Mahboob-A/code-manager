
FROM postgres:15-bullseye

# this is done for self-hosting database and backups
COPY ./docker/dev/postgres/maintenance /usr/local/bin/maintenance


RUN chmod +x /usr/local/bin/maintenance/* 

RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
        && rmdir /usr/local/bin/maintenance

