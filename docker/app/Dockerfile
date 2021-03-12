FROM python:3.7

# Set working directory
WORKDIR /var/www

# Install dependencies
COPY pyproject.toml /var/www/pyproject.toml
COPY poetry.lock /var/www/poetry.lock
RUN pip3 install poetry
RUN poetry install --no-dev

COPY ./app /var/www/app
COPY ./config /var/www/config
COPY manage.py boot.sh /var/www/

# run time configuration
EXPOSE 5000
ENTRYPOINT ["/var/www/boot.sh"]