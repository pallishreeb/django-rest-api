python -m virtualenv venv - create env

First, ensure you have Python and Django installed. If not, you can install them using pip:
pip install django djangorestframework


1. create your Django project and app
django-admin startproject bookstore
cd bookstore
django-admin startapp books

Add rest_framework and books to your INSTALLED_APPS in bookstore/settings.py.

2. Database Configuration
For now, we'll use SQLite, which is the default database for Django. Modify your DATABASES setting in bookstore/settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}


3. Create the Book model in books/models.py:

4. Create serializers for the Book model in books/serializers.py:

5. Views and URLs
Define your API views in books/views.py:

Create URL routing for the API in books/urls.py:

Include the app URLs in the main bookstore/urls.py:

pip install django-storages boto3
python -m pip install Pillow

6. Configure AWS S3 in bookstore/settings.py:

Create bookstore/storage_backends.py


7. Logging
Configure logging in bookstore/settings.py:

8. API Documentation
Install drf-yasg for API documentation:

pip install drf-yasg


Add documentation URLs in bookstore/urls.py:

9. Dockerization
Create a Dockerfile:

Create a docker-compose.yml:

10. Kubernetes Deployment
Create Kubernetes deployment and service files.

11. CI/CD with GitHub Actions
Create a .github/workflows/deploy.yml:


python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

Start the Development Server:
python manage.py runserver



admin
admin@gmail.com
Admin1234


Create a requirements.txt File
Ensure you have a requirements.txt file with all the dependencies needed for your Django project. You can generate this file by running:

pip freeze > requirements.txt

pip install --upgrade -r requirements.txt

docker-compose build
docker-compose up

docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser


---------------------------------------------------------------
Deploy Dockerize container on AWS EC2
Connect to your instance via SSH.
Install Docker on the EC2 Instance
Update the package database:

sudo apt-get update
sudo apt-get install -y docker.io
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

transfer project from local to ec2.
go to project directory
Build and run your Docker containers

sudo docker-compose up --build -d

Notes:
sudo: Runs the command with superuser privileges, which is often required for Docker commands.
docker-compose: The Docker Compose command.
up: Creates and starts the containers.
--build: Builds images before starting containers.
-d: Runs containers in detached mode.

-d Flag
The -d flag stands for "detached mode." When you run docker-compose up with the -d flag, Docker Compose will start the containers in the background and print the container IDs. This allows you to continue using your terminal session without being attached to the container's output.

Port Mapping: 8000:8000
The port mapping syntax 8000:8000 is used to map a port on the host machine to a port on the container. The general syntax is HOST_PORT:CONTAINER_PORT.

-------------------------------------------------
# Running docker image on aws ec2 automatically
integrate cicd with github action.
write deploy.yml file 
Add your EC2 instance SSH key to the GitHub secrets:
Go to your GitHub repository.
Settings > Secrets > Actions > New repository secret.
Name: EC2_SSH_KEY, Value: (paste your private SSH key)


Make changes to your application code.
Push the changes to the main branch of your GitHub repository.
GitHub Actions will automatically build the Docker image, transfer the files to the EC2 instance, and restart the Docker containers.
every time you push changes to your main branch, the deployment process on the EC2 instance is automated.



flow 1- 
Code - docker  - github - github action/jenkins - EC2(install docker to run docker image)/EKS,ECS


flow 2-
Code - docker - docker hub(registry) - github - github action - AWS EC2(install docker to run docker image)/EKS,ECS

-----------------------------------------------------

step 1- Code
Develop your application locally.

step 2 -Docker
Create Dockerfile and docker-compose.yml.
Build and test your Docker image locally.

step 3- Docker Hub (Registry)

Push your Docker image to Docker Hub or any other container registry (like AWS ECR).

step 4 -GitHub

Push your code to a GitHub repository.

step 5- GitHub Actions

Set up a GitHub Actions workflow that:
Builds your Docker image.
Pushes the Docker image to Docker Hub (or another registry).


step 6 - AWS EC2
Deploys the updated Docker image to your AWS EC2 instance.
Ensure Docker is installed and running on your EC2 instance.
Pull and run the Docker image from Docker Hub (or another registry).

# Update Package Index:
sudo apt update

# Install Prerequisite Packages:
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y

# Add Docker’s Official GPG Key:
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Set Up the Stable Repository:
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update the Package Index Again:
sudo apt update


# Install Docker:
sudo apt install docker-ce docker-ce-cli containerd.io -y

# Start Docker:
sudo systemctl start docker

# Enable Docker to Start at Boot:
sudo systemctl enable docker

# Add Your User to the Docker Group:
sudo usermod -aG docker $USER

*you'll need to log out and log back in for this change to take effect.

# Pull the Docker Image:
docker pull pallishreeb/django-api-cicd:latest

# Run the Docker Image:
docker run -d -p 80:8000 pallishreeb/django-api-cicd:latest
This command maps port 80 on your EC2 instance to port 8000 inside the Docker container.
------------------------------------
# If getting permission error in github action
Add the EC2 user to the Docker group:
sudo usermod -aG docker $USER
newgrp docker

sudo service docker restart

--------------------------------------
# To create new admin users in ec2 for djanago app-:
# List all running containers to find the container ID or name
sudo docker ps

# Access the running container (replace <container_id> with the actual ID or name)
sudo docker exec -it <container_id> /bin/bash

# Create a new superuser
python manage.py createsuperuser


-------------------------------------------
# If you want to run multiple dockers container
When transitioning to using a MySQL database, using Docker Compose is generally a better approach. Docker Compose allows you to define and manage multiple services,
including your application and its database, in a single file. This setup makes it easier to orchestrate the start-up and interaction of your services.
# Install Docker Compose:
sudo apt install docker-compose -y
OR
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version

# Create a docker-compose.yml file:
version: '3.8'

services:
  db:
    image: mysql:8.0
    volumes:
      - db_data:/var/lib/mysql
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: mydatabase
      MYSQL_USER: myuser
      MYSQL_PASSWORD: mypassword

  web:
    image: pallishreeb/django-api-cicd:latest
    command: python manage.py runserver 0.0.0.0:8000
    ports:
      - "80:8000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=mysql://myuser:mypassword@db:3306/mydatabase
      - ALLOWED_HOSTS=your-ec2-public-ip-or-dns

volumes:
  db_data:

# Update django project setting
pip install dj-database-url

Update your Django settings to use the MySQL database. Replace the DATABASES setting in your settings.py:
import os
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}

# Change Script under Deploy in github deploy.yml
    script: |
          cd /path/to/your/project  # Ensure you are in the correct directory
          sudo docker-compose pull
          sudo docker-compose down
          sudo docker-compose up -d