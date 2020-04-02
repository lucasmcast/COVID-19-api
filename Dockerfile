FROM python:3.6-alpine

ENV FLASK_APP flasky.py
ENV FLASK_CONFIG docker

RUN adduser -D flasky
USER flasky

WORKDIR /home/flasky

COPY requeriments requeriments
RUN python -m venv venv
RUN venv/bin/pip install -r requeriments/docker.txt

COPY app app
COPY migrations migrations
COPY flasky.py config.py enginer_db.py interval_runner.py boot.sh ./

#configuração para execução
EXPOSE 5000
CMD ["source venv/bin/activate"]
CMD ["flask deploy"]
CMD ["exec gunicorn -b :5000 --access-logfile - --error-logfile - flasky:app"]