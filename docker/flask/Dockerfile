FROM python:3.9.12

ARG APP_HOME=/home/aaas
RUN apt-get update \
  && apt-get install --no-install-recommends --yes supervisor

# accept arguments
ARG PIP_REQUIREMENTS=requirements.txt

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip setuptools

# set work directory
WORKDIR ${APP_HOME}

COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY proxy_server.py .

CMD ["python","proxy_server.py"]