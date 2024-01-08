FROM python:3.10.5
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ENV DEV_ENV 1

RUN mkdir /code
WORKDIR /code

COPY requirements /code/
RUN pip install -r requirements_dev.txt

COPY . /code/

RUN rm -r frontend & useradd -m -d /code -s /bin/bash -u 1001 -U app
RUN chown -R app:app /code 
USER 1001
