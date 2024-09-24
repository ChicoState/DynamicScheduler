FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    build-essential \
    nginx \
    curl \
    sudo

COPY utils/requirements.txt .
RUN pip3 install -r requirements.txt

RUN rm /etc/nginx/sites-enabled/default
COPY utils/nginx.conf /etc/nginx/sites-enabled/default

COPY . /app

WORKDIR /app

EXPOSE 80

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:5000 wsgi:app & nginx -g 'daemon off;'"]
