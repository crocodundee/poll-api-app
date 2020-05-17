# Poll API
_A Web API for the passage of polls_
### _Before you start:_
I used Docker to build this app and it requires to install some dependencies to manage this project on your local machine. So be confident in your OS (Windows 10 Pro or any Unix system) which has installed packeges of [python3](https://www.python.org/downloads/), [git](https://www.atlassian.com/git/tutorials/install-git), [Docker](https://docs.docker.com/get-docker/).
### _Requirements:_
* Django 2.2.10
* Django REST Framework 3.9.4
* psycopg2
* flake8
### _Lets begin!_
1. Clone this repository to your local machine
      ```
      git clone http://github.com/crocodundee/poll-api-app.git
      ```
2. Build Docker container with 
    ```
    docker-compose build
    ```
3. Init database schema with
    ```
    docker-compose tun ap sh -c "python manage.py makemigrations"
    ```
4. Create admin to manage polls
    ```
    docker-compose run app sh -c "python manage.py createsuperuser"
    ```
5. Run project and view API documentation in your browser on _0.0.0.0:8000_ :
    ```
    docker-compose up
    ```
### _Try it :point_right: [the-poll-api-app](https://the-poll-api-app.herokuapp.com)_
