# Django Web Application: User Login, CSV Upload, and Database Filtering


# Description
This Django web application allows users to log in, upload data from a CSV file to a PostgreSQL database, apply filters to the database using a form, and display the count of records based on the applied filters.

# Installation
1. Clone the repository:
clone https://github.com/Kiran4725/Catalyst.git

2. Navigate to the project directory:
cd yourproject

3. Create and activate a virtual environment:
python3 -m venv env
env\Scripts\activate

4. Install the required packages:
pip install -r requirements.txt

5. Configure PostgreSQL database:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'yourdbname',
        'USER': 'yourdbuser',
        'PASSWORD': 'yourdbpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

6. Apply database migrations:
python manage.py migrate

7. Run the Django development server:
python manage.py runserver

