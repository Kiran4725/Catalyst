# Catalyst Count

# Description
This Django web application allows users to log in, upload data from a CSV file to a PostgreSQL database, apply filters to the database using a form, and display the count of records based on the applied filters.

# Installation
1. Clone the repository:
   
    clone https://github.com/Kiran4725/Catalyst.git

3. Navigate to the project directory:

    cd Catalyst_Count

4. Create and activate a virtual environment:
   
    python3 -m venv env
   
    env\Scripts\activate

6. Install the required packages:

    pip install -r requirements.txt

7. Configure PostgreSQL database:

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

8. Run the Django development server:
   
    python manage.py runserver
   
# Output

1.Login Page

   ![login](https://github.com/user-attachments/assets/60da0dcd-13c4-4569-9b85-886bea50e727)


2. Registration Page
   
   ![registration](https://github.com/user-attachments/assets/18b84004-f395-4a7b-9030-f74649e2d0ab)

3. Upload Data
   
   ![upload_data](https://github.com/user-attachments/assets/b76a8ada-b77e-4d4d-a45d-7bb147cb1662)

4. Query Builder

   ![query_builder](https://github.com/user-attachments/assets/287ca8b8-c9db-40e4-a7ce-1790b8859fb5)


5. Users
   
   ![users](https://github.com/user-attachments/assets/643bb5ef-ea26-461d-81fb-15f9d70b4376)



