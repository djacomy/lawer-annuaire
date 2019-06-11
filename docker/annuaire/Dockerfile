FROM registry.gitlab.com/juripredis/juripredis-baseimage-docker/python-3.7

USER root

# we copy just the requirements.txt first to leverage docker cache
COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn

COPY --chown=juripredis:juripredis . /app

RUN chown juripredis:juripredis /app && \
    chmod 744 /app

USER juripredis

# run the app with app server
CMD [ "gunicorn", "-c", "gunicorn.conf", "manage:app" ]
