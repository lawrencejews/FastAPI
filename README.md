### FastAPI - Python API Development.

#### NOTE - creating a user is key to use this repo: 
- First create a user for login to access the endpoints OR you will get `Not Authenticated Error`.

####  Setting up development environment.`CRUD`
- Create a virtual environment for the project.
- Activate environment in the project folder `source venv/bin/activate .`
- Build this project off `FASTAPI`- `fastapi.tiangolo.com`.
- Packages for FASTAPI - `pip install fastapi` && `pip install "uvicorn[standard]"`.
- OR install all packages at once with `pip install "fastapi[all]"`.
- Start the server for SQL queries: `uvicorn app.mainsql:app --reload`.
- Start the server for NO-SQL queries: `uvicorn app.mainnosql:app --reload`.
- To check your endpoint run: `http://127.0.0.1:8000/docs` to start the openapi.json for fastapi.
- The pydantic library is used for data validation when creating schemas in a python application.
- Create a python package use `__init__.py` in the folder of choose.
- Psycopg driver for PostgresSQL to implement a complete Python DB API NOT for windows
  ```
  sudo apt install python3-dev libpq-dev && pip install psycopg2 
  
  ```
- Object Relational Mapper-ORM - using `sqlalchemy` and `psycopg2` drivers to access data from the database.

#### Authentication & Routing
- Postman auth: run the login endpoint and set the environment variable from test `pm.environment.set("JWT", pm.response.json().access_token)` to automate the process.
- Create routes between the client, API and the database.
- APIRouter acts as the bridge for connection of different route endpoints.
- Fastapi passlib package hashes the passwords stored in the database ` pip install passlib'[bcrypt]' `
- The token is shared for authentication through hashing of the secret.
- Token verification using the header, signature and payload.
- Fastapi uses python-jose for Oauth2-JWT password encryption `pip install python-jose'[cryptography]'  `

#### Migration
- Track changes to the code and rollback with GIT.
- Database migration allows incremental changes to the database schema and rollback changes anytime.
- Alembic is a tool used to make automated pull of models from sqlalchemy and generate proper tables.
- Alembic.sqlalchemy `https://alembic.sqlalchemy.org/en/latest/tutorial.html`.
- Initialize alembic `alembic init DIRECTORY_NAME`
- Give alembic access to the `BASE` from the models file.
- Create Posts table `alembic revision -m "create posts table"`.
- Alembic upgrade connects to the database creating a new column `alembic revision -m "add content column to posts table"`
- Alembic's autogenerate function to update the schemas with the provided models `alembic revision --autogenerate -m TABLE_NAME`.

#### CORS - Cross Origin Resource Sharing
- Allows to make requests from a web browser on one domain to a server on a different domain.
- Web browsers by default allow API running on the same domain to make requests to the server.