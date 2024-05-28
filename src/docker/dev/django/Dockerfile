ARG PYTHON_VERSION=3.10-bullseye 


FROM python:${PYTHON_VERSION} as python 

# stage 01: build dependency wheel 
FROM python as python-build-stage 

ARG BUILD_ENVIRONMENT=dev 

RUN apt-get update && apt-get install --no-install-recommends -y \
        build-essential

COPY ./requirements . 

RUN pip wheel --wheel-dir /usr/src/app/wheel \
        -r ${BUILD_ENVIRONMENT}.txt 


# stege 02: run the app 

FROM python as python-run-stage 

# args 
ARG BUILD_ENVIRONMENT=dev 
ARG APP_HOME=app 

# env 
ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONUNBUFFERED 1 
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install --no-install-recommends -y \
        gettext \
        && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
        && rm -rf /var/lib/apt/lists/* 


COPY --from=python-build-stage /usr/src/app/wheel /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
        && rm -rf /wheels/

# entrypoint script is to check db status 
COPY ./docker/dev/django/entrypoint /entrypoint

RUN sed -i 's/\r$//g' /entrypoint

RUN chmod +x /entrypoint 

# start script is to start the dev server and consuming messages 
COPY ./docker/dev/django/start.sh /app/docker/dev/django/start 

RUN sed -i 's/\r$//g' /app/docker/dev/django/start

RUN chmod +x /app/docker/dev/django/start

COPY . ${APP_HOME}

ENTRYPOINT [ "sh", "/app/docker/dev/django/start.sh" ]
