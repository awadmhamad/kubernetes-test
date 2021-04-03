FROM python:3.9-alpine
WORKDIR /usr/src/app

RUN pip install PyGithub

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 pip install psycopg2

COPY . .

CMD [ "python", "main.py" ]

