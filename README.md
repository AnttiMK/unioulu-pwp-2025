# PWP SPRING 2025

# Burgir™ Restaurant Order Management System

# Group information

* Student 1. Antti Koponen, <antti.koponen@student.oulu.fi>
* Student 2. Eemeli Huotari, <eemeli.huotari@student.oulu.fi>
* Student 3. Matias Paavilainen, <matias.paavilainen@student.oulu.fi>
* Student 4. Markus Teuhola, <markus.teuhola@student.oulu.fi>

__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint, instructions on how to setup and run the client, instructions on how to setup and run the axiliary service and instructions on how to deploy the api in a production environment__

-----
## Setting up development environment
```bash
# Create virtual environment
python -m venv .venv

# Windows
.\.venv\Scripts\activate

# Unix
source .venv/bin/activate

pip install -r requirements.txt
```

## Creating & populating the database
```bash
python manage.py migrate
python prepopulate.py
```
Alternatively, you can populate the database manually through the Django Admin Panel.
```bash
python manage.py createsuperuser
```

Log in with the newly created credentials at the /admin endpoint.

**In the project, a model must be registered to admin.py to edit its content in the admin panel!**
## Running Django development server
```bash
python manage.py runserver
```

-----

## Development commands
```bash
# Migrations must always be generated when changes are made to the models.
python manage.py makemigrations
python manage.py migrate
```
```bash
# Project uses pylint for linting
pylint app
```
```bash
# Tests can be run with coverage to automatically generate a coverage report
coverage run manage.py test
coverage html
```
