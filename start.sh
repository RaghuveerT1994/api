#!/bin/bash

# If the application type is API then start application
if [ ${APP_TYPE} == 'BG' ]
then
  # Assigning system environment variables to supervisor environment
  printenv >> /etc/environment

  echo "environment=DB_HOST='${DB_HOST}',
        DB_USER='${DB_USER}',
        DB_PASSWORD='${DB_PASSWORD}',
        DB_NAME='${DB_NAME}',
        DB_PORT='${DB_PORT}',
        UI_URL='${UI_URL}',
        API_URL='${API_URL}',
        MANUAL_EMAIL='${MANUAL_EMAIL}',
        SEND_EMAIL_HOST='${SEND_EMAIL_HOST}',
        SEND_EMAIL_PORT='${SEND_EMAIL_PORT}',
        SEND_EMAIL_ADDRESS='${SEND_EMAIL_ADDRESS}',
        SEND_EMAIL_PASSWORD='${SEND_EMAIL_PASSWORD}',
        MANUAL_EMAIL_HOST='${MANUAL_EMAIL_HOST}',
        MANUAL_EMAIL_PORT='${MANUAL_EMAIL_PORT}',
        MANUAL_EMAIL_HOST_USER='${MANUAL_EMAIL_HOST_USER}',
        MANUAL_EMAIL_HOST_PASSWORD='${MANUAL_EMAIL_HOST_PASSWORD}'" >> background.conf

  # Moving background process config file to supervisor config location
  cp -R /var/opt/background.conf /etc/supervisor/conf.d/

  # Start supervisor service
  service supervisor start

  # Update supervisor config
  supervisorctl update

  # open supervisor error log
  tail -f /var/log/long.err.log
else

  # python3 manage.py collectstatic

  printenv >> /etc/environment

  chmod 0644 /etc/cron.d/project_allocation-cron

  crontab /etc/cron.d/project_allocation-cron

  service cron start

  python3 manage.py migrate

  uwsgi --emperor /etc/uwsgi/vassals --uid root --gid root --enable-threads --daemonize /var/opt/media/uwsgi-emperor.log

  service nginx restart
fi
