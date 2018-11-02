FROM python:3.6
EXPOSE 8000

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt
COPY . /app
ENV DATABASE_URL postgres://postgresql:postgresql@db:5432/adhesion2
ENV SECRET_KEY ''
ENV DJANGO_ENV ''
CMD exec yes yes | python3 manage.py migrate && python3 manage.py collectstatic --noinput && gunicorn mapp.wsgi -b 0.0.0.0:8000 --log-file -