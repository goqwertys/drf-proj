# Running a Project with Docker Compose  
This project uses Docker Compose to run several services, including Django, PostgreSQL, Redis, Celery, and Celery Beat. Below are the steps to run the project and check that each service is running.  
***  
### Steps to Launch a Project  
1. #### Make sure you have Docker and Docker Compose installed:
 - [Installing Docker](https://docs.docker.com/get-started/get-docker/)  
 - [Installing Docker Compose](https://docs.docker.com/compose/install/)  
2. #### Clone the repository:  
	```
	git clone <ваш-репозиторий>
	cd <ваш-репозиторий>
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
