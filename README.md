# Task Manager API 

It is a fully containerized backend REST API built using FastAPI, *SQLAlchemy*, and *PostgreSQL*. 

It secures user authentication, team collaboration, project grouping, and task management. The entire application is packaged cleanly inside Docker and is live on the cloud.

##  Live Production URL
* Swagger UI: **https://task-manager-api-ekuw.onrender.com/docs**

## My Tech Stack
* Framework: FastAPI (Python 3.11) 
* Database: PostgreSQL 
* ORM & Migrations: SQLAlchemy (Object-Relational Mapper) & Alembic 
* Containerization: Docker & Docker Compose
* Hosting Platform: Render 

## Repository Structure
Here is how I organized the files and directories in this project:

├── app/
│   ├── main.py            
│   ├── core/             
│   ├── models/           
│   ├── routes/         
│   ├── schemas/         
│   └── auth/            
├── alembic/            
├── .dockerignore        
├── .env.example          
├── docker-compose.yml    
├── Dockerfile            
└── requirements.txt      