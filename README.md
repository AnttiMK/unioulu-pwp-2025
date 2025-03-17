# PWP SPRING 2025

# Burgir™ Restaurant Order Management System

# Group information

* Student 1. Antti Koponen, <antti.koponen@student.oulu.fi>
* Student 2. Eemeli Huotari, <eemeli.huotari@student.oulu.fi>
* Student 3. Matias Paavilainen, <matias.paavilainen@student.oulu.fi>
* Student 4. Markus Teuhola, <markus.teuhola@student.oulu.fi>

__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint, instructions on how to setup and run the client, instructions on how to setup and run the axiliary service and instructions on how to deploy the api in a production environment__

## Setting up environment

```bash
python -m venv .venv

# Windows
.\.venv\Scripts\activate

# Unix
source .venv/bin/activate

pip install -r requirements.txt
```

## Create the database (if it doesn't exist)

```bash
python manage.py migrate
```

## The following commands must be run whenever adding or making changes to database models

```bash
python manage.py makemigrations
python manage.py migrate
```

## Run Django development server

```bash
python manage.py runserver
```

## Run pylint

```bash
pylint app
```

## Run tests

```bash
python manage.py test
```

## Pre-populate the database with a script

After creating the database and the tables through the __migrate__ command, run

```bash
python prepopulate.py
```

to create dummy data for all tables.

## Populate the database manually through the Django Admin Panel

Run this command to create credentials that can be used for the admin panel:

```bash
python manage.py createsuperuser
```

Log in with the newly created credentials at the /admin endpoint.

__In the project, a model must be registered to admin.py to edit its content in the admin panel!__
