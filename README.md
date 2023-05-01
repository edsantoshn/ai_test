#  Magic's Kingdom Docs System!

This is a demo to solve the necessity of Magic Kingdom, using FastAPI as a framework.


# Requirements

You need to install first Pipenv to install all the dependencies.

**Installing Pipenv**

    pip install pipenv or pip3 install pipenv
 
 **Go to repository folder**

     cd ai_test

## Database server

You need a MySQL server to deploy the database and create a database could be ai_test or your custom name as well. if you don't have the MySQL you can use docker like the next sentence

    docker run --name <ur_container_name> -p 3306:3306 -e MYSQL_ROOT_PASSWORD=<ur_password> -d mysql:latest

you must change the <**ur_container_name**> to your custom name and  <**ur_password**> for a security password.

Now you have to create a Database if you prefer you can use a software to connect to DB server. this name will be use it to SQLALCHEMY_DATABASE_URI

## Rename template.env
In the root project path you will be find a template.env file you have to change the name to .env only.  After you create the Database will be create a variable like next.

    SQLALCHEMY_DATABASE_URI=mysql+pymysql://{user}:{ur_password}@{host}:{port}/{db_name}

The default **user** is root, the **password** (if you are follow this tutorial step by step is the password used on Database Server), **host** where the db server is 127.0.0.1, localhost or other address, **port** where your server is listen 3306 by default but may be you changed finally you need the db_name the same name you create before.

**SECRET_KEY** this is a mandatory variable to encrypt and decrypt the JWT. 32 bits, you can use a simple text or generate by openssl in your console.

    openssl rand -hex  16

**ALGORITHM** the algorithm use to encrypt and decrypt.

**ACCESS_TOKEN_EXPIRE_MINUTES** the expiration time of your access token, must be a integer.

## Installing all the dependencies

 this code create first the virtual environment and install all the dependencies from pipenv file.

    pipenv install

## Start the server

To start the server you have to verify if you are in the root project folder to do that try to find main.py 
on linux and mac

ls

on windows 

    dir
now you must activate the virtual env with pipenv

    pipenv shell

and finally start the server 

    python main.py
this command in the first time will be create Grimoire, MagicAffinity and User, the user by default will be:

    Username: test, Password: password123.

## Access to the Endpoint
To access to the endpoint you have two option:

 1. OpenAPI Documentation (e.g. 127.0.0.1:8000/docs)
 2. ReDocumentation (e.g. 127.0.0.1:8000/redoc)

if you prefer Postman or Insomia you could use them as well.

**Note:** second time using the api you have to make only the start server steps and Access to the endpoint.