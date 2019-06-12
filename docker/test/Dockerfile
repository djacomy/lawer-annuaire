FROM registry.gitlab.com/juripredis/juripredis-baseimage-docker/python-3.7

USER root

RUN apt-get update  && apt-get install -y --no-install-recommends poppler-utils \
      && apt-get clean \
      && rm -rf /var/lib/apt/lists/*

# we copy just the requirements.txt first to leverage docker cache
COPY requirements.txt /app/requirements.txt
COPY requirements_tests.txt /app/requirements_tests.txt

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt  -r requirements_tests.txt

COPY --chown=juripredis:juripredis . /app

RUN chown juripredis:juripredis /app && \
    chmod 744 /app

USER juripredis

# run the app with app server
CMD [ "python", "-m", "manage", "runserver",  "-h",  "0.0.0.0", "-p", "5000",  "-d"]

