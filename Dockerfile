FROM python:3.12.3-slim 

ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONUNBUFFERED=1 

WORKDIR /app 

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

COPY requirements.txt /app/ 
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt 

COPY . /app/

EXPOSE 8000

CMD [ "python manage.py runserver 0.0.0.0:8000" ]
