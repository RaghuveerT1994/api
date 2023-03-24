FROM ubuntu:22.04

MAINTAINER Raghu T  <raghu.t@iopex.com>

# Application env variables

# Add a new user "iopex" with user id 3333
RUN useradd -ms /bin/bash -u 3333 iopex

# Install dependencies
RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    vim \
    wget \
    curl \
    python3 \
    python3-dev \
    python3-pip \
    libmysqlclient-dev \
    python3-pymysql \
    libleptonica-dev \
    python3-unidecode \
    language-pack-en \
    nginx \
    python3-setuptools python3-opencv poppler-utils libssl-dev \
    # python python-dev supervisor \
    gnupg2 \
    cron \
    openssl \
    #wkhtmltopdf \
    ca-certificates

# RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb

# RUN apt install -y ./wkhtmltox_0.12.6-1.focal_amd64.deb

# RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

# RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

# RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# RUN apt-get update && apt-get install -y unixodbc-dev

RUN apt-get update && apt-get install -y python3-dev libmysqlclient-dev

WORKDIR /var/opt

COPY . /var/opt

RUN python3 -m pip install --upgrade pip && pip install -r requirements.txt

# Change to non-root privilege
# USER iopex
ENV MANUAL_EMAIL mail.test2@iopex.com

ENV MANUAL_EMAIL_HOST mail2.iopex.com
ENV MANUAL_EMAIL_PORT 587
ENV MANUAL_EMAIL_HOST_USER mail.test2@iopex.com
ENV MANUAL_EMAIL_HOST_PASSWORD iopex@123

RUN rm -rf /var/opt/media

RUN rm -rf /var/opt/db_data

RUN mkdir media

RUN mkdir media/log

# RUN mkdir /var/opt/media/sample

# ADD ./media/sample/* /var/opt/media/sample/

# RUN mv -f /var/opt/opexwise/settings.py.dist /var/opt/opexwise/settings.py

RUN export LC_ALL="en_US.UTF-8"

RUN mkdir -p /etc/uwsgi/sites

RUN mkdir /etc/uwsgi/vassals

RUN ln -s /var/opt/project_allocation.ini /etc/uwsgi/vassals/

RUN mv -f /var/opt/nginx/default /etc/nginx/sites-available/

RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# Change to executeable mode
RUN chmod a+x /var/opt/background.sh
RUN chmod a+x /var/opt/start.sh

# Add cron file
COPY project_allocation-cron /etc/cron.d/project_allocation-cron

EXPOSE 80

HEALTHCHECK CMD (pgrep -f nginx | pgrep -f background.sh) || exit 1

ENTRYPOINT ["./start.sh"]
