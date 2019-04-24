FROM python:3.6

# Set working directory
WORKDIR /var/www

# Install dependencies
COPY requirements /var/www/requirements
RUN pip3 install -r requirements/docker.txt

COPY ./app /var/www/app
COPY ./config /var/www/config
COPY manage.py boot.sh /var/www/

# run time configuration
EXPOSE 5000
ENTRYPOINT ["/var/www/boot.sh"]