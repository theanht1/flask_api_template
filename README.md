[![Build Status](https://travis-ci.com/theanht1/flask_api_template.svg?branch=master)](https://travis-ci.com/theanht1/flask_api_template)
[![Coverage Status](https://coveralls.io/repos/github/theanht1/flask_api_template/badge.svg?branch=master)](https://coveralls.io/github/theanht1/flask_api_template?branch=master)

# Introduction
Simple framework for building REST API with Flask 

## Installation
#### Python virtual environment
```shell script
python3 -m venv venv
source venv/bin/activate
```
or Conda
```shell script
conda create --name python3.7 python=3.7
conda activate python3.7
```

#### Lib dependencies
```
pip install poetry
poetry install
```

## Usage
Configure the environment variables in folder `/config`

Run the flask app
```
python run.py [port]
```
 
 ## Run with docker
 You can use docker instead of the above Installation & Usage steps.
 
 Check port's availability
 ```
 $ sudo nc localhost <port number> < /dev/null; echo $?
 ```

 
 Update `docker-compose.yml` file to connect nginx webserver to host's port
 ```
 webserver:
    ...
    
    ports:
      - '8000:80'
    networks:
      - app-network
    
    ...
 ```
 
 Run the docker daemon
  ```
 $ docker-compose up -d
 ```
 
 Check docker container
 ```
 $ docker ps -a
 ```
 
## Test

Run test
```
coverage run -m pytest
```

See the test coverage report
```
coverage report
```
