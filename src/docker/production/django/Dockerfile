# 080624, Saturday, 08.00 pm 

ARG PYTHON_VERSION=3.10-bullseye 


FROM python:${PYTHON_VERSION} as python 

# stage 01: build dependency wheel 
FROM python as python-build-stage 

ARG BUILD_ENVIRONMENT=production

RUN apt-get update && apt-get install --no-install-recommends -y \
        build-essential

COPY ./requirements . 

RUN pip wheel --wheel-dir /usr/src/app/wheel \
        -r ${BUILD_ENVIRONMENT}.txt 


# stege 02: run the app 

FROM python as python-run-stage 

# creating an user (codemanageris the user and group)
RUN addgroup --system codemanager && adduser --system --ingroup codemanager codemanager

# args 
ARG BUILD_ENVIRONMENT=production

# app home 
ARG APP_HOME=/home/codemanager/app

# env 
ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONUNBUFFERED 1 
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

#  staticfiles and mediafiles dir, permissions of the dir to the user. 
RUN mkdir -p ${APP_HOME}/staticfiles ${APP_HOME}/mediafiles && \
        chown -R codemanager:codemanager ${APP_HOME}/staticfiles ${APP_HOME}/mediafiles && \
        chmod -R 775 ${APP_HOME}/staticfiles ${APP_HOME}/mediafiles

        
RUN apt-get update && apt-get install --no-install-recommends -y \
        libpq-dev \
        gettext netcat \
        && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
        && rm -rf /var/lib/apt/lists/* 


COPY --from=python-build-stage /usr/src/app/wheel /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
        && rm -rf /wheels/



# entrypoint script is to check db status. copy as user 
COPY --chown=codemanager:codemanager ./docker/production/django/entrypoint /entrypoint

RUN sed -i 's/\r$//g' /entrypoint

# checks the postgres db availability 
RUN chmod +x /entrypoint 

# start script is to start the production server using gunicorn on port 8001 and consuming messages 
COPY --chown=codemanager:codemanager ./docker/production/django/start /start

RUN sed -i 's/\r$//g' /start

RUN chmod +x /start

COPY --chown=codemanager:codemanager . ${APP_HOME}

# ownership of APP_HOME
RUN chown codemanager:codemanager ${APP_HOME}

USER codemanager

ENTRYPOINT ["/entrypoint"]
