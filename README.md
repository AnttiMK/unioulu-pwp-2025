# PWP SPRING 2025
# Burgir™ Restaurant Order Management System
# Group information
* Student 1. Antti Koponen, antti.koponen@student.oulu.fi
* Student 2. Eemeli Huotari, eemeli.huotari@student.oulu.fi
* Student 3. Matias Paavilainen, matias.paavilainen@student.oulu.fi
* Student 4. Markus Teuhola, markus.teuhola@student.oulu.fi


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

## Populate the database through the Django Admin Panel
```bash
python manage.py createsuperuser
```
Log in with the newly created credentials to the /admin endpoint.

**Register a model to admin.py to edit its content in the admin panel!**
