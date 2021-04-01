FROM python:3.9-slim-buster

WORKDIR /usr/src/app

RUN pip install PyGithub

COPY . .

CMD [ "python", "main.py" ]

