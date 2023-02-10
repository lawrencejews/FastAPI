### FastAPI - Python API Development.
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
- Postman auth: run thee login endpoint and set the environment variable from test `pm.environment.set("JWT", pm.response.json().access_token)` to automate te process.
- Create routes between the client, API and the database.
- APIRouter acts as the bridge for connection of different route endpoints.
- Fastapi passlib packages hashes the passwords stored in the database ` pip install passlib'[bcrypt]' `
- The token is shared for authentication through hashing of the secret.
- Token verification using the header, signature and payload.
- Fastapi uses python-jose for Oauth2-JWT password encryption `pip install python-jose'[cryptography]'  `

#### Migration
