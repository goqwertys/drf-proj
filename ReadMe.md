
# Deploying a Django Application Using GitHub Actions
This repository contains a Django application with a configured CI/CD pipeline for automatic linting, testing, building a Docker image, and deploying to a remote server.
***
### Table of Contents
1. [Requirements](#requirements)
2. [Setting up a remote server]()
3. [Setting up secrets in GitHub]()
4. [Starting deployment]()
5. [Checking the application operation]()
***
### Requirements
For a successful deployment you will need:
* Remote server with Docker installed.
* Docker Hub account.
* Access to the repository on GitHub.
***
### Setting up a remote server
1. #### Install Docker
   You must have Docker installed on your server. Run the following commands:
   ```
   sudo apt update
   sudo apt install -y docker.io
   sudo systemctl enable docker
   sudo systemctl start docker
   ```
2. #### Set up SSH access
   1. Create an SSH key on your local machine (if you don't have one):
      ```
      ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
      ```
   2. Copy the public key to the server:
      ```
      ssh-copy-id -i ~/.ssh/id_rsa.pub user@your-server-ip
      ```
   3. Check the connection:
      ```
      ssh -o StrictHostKeyChecking=no user@your-server-ip
      ```
***
### Setting up secrets in GitHub
#### 1. Добавьте секреты в репозиторий

   Перейдите в настройки вашего репозитория на GitHub:
1.  **Settings**  →  **Secrets and variables**  →  **Actions**.
3. Add the following secrets:
      - `DOCKER_HUB_USERNAME`: Docker Hub Username.
      - `DOCKER_HUB_ACCESS_TOKEN`: Docker Hub access token.
      - `SSH_USER`: Username for SSH connection to the server.
      - `SSH_KEY`: Private SSH key to access the server.
      - `SERVER_IP`: The IP address of your server.
      - `DOTENV`: The contents of your .env file (all environment variables).
***
### Starting deployment
#### 1. Push to the repository
   После добавления секретов:
   1. Make changes to the code (for example, add new functionality).
   2. Push changes to the repository:
		```
		git add .
		git commit -m "Some new feature"
		git push origin main
		```
#### 2. Check the execution of the workflow
   1. Go to the **Actions** tab in your GitHub repository.
   2. Verify that the workflow has started and completed successfully.
***
### Checking the application operation
After successful execution of the workflow, the application will be automatically deployed to your server. You can check its availability by the server IP address:
	```
	http://your-server-ip
	```
***
### Useful commands
#### Stopping and removing a container:
If you need to stop and delete the container manually, run the following on the server:
   ```
   docker stop myapp
   docker rm myapp
   ```
#### View logs:
To view the application logs, run:
   ```
   docker logs myapp
   ```
***
# Running a Project with Docker Compose (old)
This project uses Docker Compose to run several services, including Django, PostgreSQL, Redis, Celery, and Celery Beat. Below are the steps to run the project and check that each service is running.  
***  
### Steps to Launch a Project  
1. #### Make sure you have Docker and Docker Compose installed:
 - [Installing Docker](https://docs.docker.com/get-started/get-docker/)  
 - [Installing Docker Compose](https://docs.docker.com/compose/install/)  
2. #### Clone the repository:  
	```
	https://github.com/goqwertys/drf-proj.git
	cd my-drf-project
	```
 3. #### Create a .env file  
  
      - Copy the example file .env.example to `.env`:
		```
		cp .env.example .env
		```
	
	- Edit `.env` to specify the necessary settings (for example, database passwords).

3. #### Launch the project:  
  
   - Using command:
	   ```
	   docker-compose up --build
	   ``` 
	- This command will build and run all services described in `docker-compose.yml`
4. #### Project stop:
	- To stop the project, run:
		```
		docker-compose down
      ```
***  
### Checking the functionality of services

After launching the project, you can check the functionality of each service.

  1. #### Django (web server):
     - Connect to the database from the `app` container:
        ```
       docker-compose exec app bash
       psql -h db -U postgres -d drf-db
       ```
        
     - If the connection is successful, you will be taken to the interactive PostgreSQL console.

 2. #### PostgreSQL (database):
    - Connect to the database from the `app` container:
      ```
      docker-compose exec app bash
      psql -h db -U postgres -d drf-db
      ```
    - If the connection is successful, you will be taken to the interactive PostgreSQL console.
 3. #### Redis (broker for Celery):
    - Check that Redis is running:
      ```
      docker-compose exec redis redis-cli ping
      ```
    - If Redis is running, you will get a `PONG` response.

 4. #### Celery (worker):
    - Check celery container logs:
      ```
      docker-compose exec redis redis-cli ping
      ```
    - Make sure there are no errors in the logs and Celery has successfully connected to Redis.
 5. #### Celery Beat (task scheduler):
    - Check the celery_beat container logs:
      ```
      docker-compose logs celery_beat
      ```
    - Убедитесь, что в логах нет ошибок и Celery Beat успешно запущен.
***  
### Project management commands:
   - **Re-creating containers**:
     ```
     docker-compose up --build
     ```
   - **Stopping the project**:
     ```
     docker-compose down
     ```
   -  **View logs of a specific service:**
      ```
       docker-compose logs <service_name>
         ```
      For example:
      ```
       docker-compose logs celery
         ``
     - **Cleaning up Docker volumes** (if you want to start from a clean state):
       ```
       docker-compose down -v
         ```
***
### Conclusion:
Your project should now be up and running. If you encounter any issues, check the logs of the relevant services using the `docker-compose logs command`.
***
