# https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/

# TODO: non-root
# TODO: dont use latest, set python version explicitly
FROM python

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /soft_serve

# Install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .

# DB Should be outside of container
# RUN python manage.py makemigrations
# RUN python manage.py migrate

# List of commands to execute
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
