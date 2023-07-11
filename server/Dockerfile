FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/server

COPY ./requirements_deploy.txt /usr/src/requirements_deploy.txt

RUN pip install -r /usr/src/requirements_deploy.txt

COPY . /usr/src/server

EXPOSE 8000

CMD python manage.py migrate
CMD python manage.py runserver 0.0.0.0:8000