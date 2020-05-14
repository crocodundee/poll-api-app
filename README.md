# base-django-project
_This repository provides a base configuration project to build applications using Django+PostgreSQL+Docker. Write robust applications from start to easy deploy!_ :smile:
### _Before you start:_
We will use Docker to build our app in container and it requires to install some dependencies. So be confident in your OS (Windows 10 Pro or any Unix system) which has installed packeges of [python3](https://www.python.org/downloads/), [git](https://www.atlassian.com/git/tutorials/install-git), [Docker](https://docs.docker.com/get-docker/).
### _You already have:_
* Django
* Django REST Framework
* psycopg2
* flake8
### _Lets begin!_
1. Clone this repository to your local machine with specific project name
      ```
      git clone http://github.com/crocodundee/base-django-project.git <you_project_dir_name>
      ```
2. Change remote repository url
    ```
    git remote set-url origin <your_repo_link>
    git add .
    git commit -am "Configure project"
    git push -f origin
    ```
3. Open source code in your favorite code editor and edit __req.txt__ file with requirements your project needs.
4. Build Docker container with 
    ```
    docker build .
    docker-compose build
    ```
5. Create custom user model (or not if you'll use it from box) and create migrations
    ```
    docker-compose run app sh -c "python manage.py makemigrations"
    ```
6. Test your code
    ```
    docker-compose run app sh -c "python manage.py test && flake8"
    ```
6. Create superuser to manage your project
    ```
    docker-compose run app sh -c "python manage.py createsuperuser"
    ```
7. Create other apps by
    ```
    docker-compose run app sh -c "python manage.py startapp <app_name>"
    ```
8. Run project and view result in your browser on _0.0.0.0:8000_ :
    ```
    docker-compose up
    ```
9. Save project changes to remote repository
    ```
    git add .
    git commit -am <commit_message>
    git push origin
    ```
