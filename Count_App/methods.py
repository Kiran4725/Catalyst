
from Count_App.models import *
import os
import csv
import pandas as pd
from django.db import transaction

basePath = os.getcwd().replace("\\","/")+"/Count_App/static"

required_fields = {
    'name': '',
    'domain': '',  
    'year founded': 0,  
    'industry': '',  
    'locality': '',
    'country': '',
    'linkedin url': ''
}

def validate_and_clean_row(row):
    """Validate and clean a single row of DataFrame data, handling missing or blank values."""
    cleaned_row = {}
    
    for field, default in required_fields.items():
        value = row.get(field, default)
        # Check if the value is None or a blank string and set the default if true
        if pd.isna(value) or value == '':
            value = default
        cleaned_row[field] = value
    
    # Process and split 'locality' field into city and state
    locality_parts = cleaned_row['locality'].split(',') if cleaned_row['locality'] else []
    if len(locality_parts) == 3:
        city = locality_parts[0].strip()
        state = locality_parts[1].strip()
    else:
        city = ''
        state = ''


    return {
        'Name': cleaned_row['name'],
        'Domain': cleaned_row['domain'],
        'YearFounded': int(cleaned_row['year founded']),
        'Industry': cleaned_row['industry'],
        'City': city,
        'State': state,
        'Country': cleaned_row['country'],
        'LinkedinUrl': cleaned_row['linkedin url']
    }

def process_csv(file):
    # Define the static folder path
    static_dir = os.path.join(basePath, 'uploads')

    # Ensure the directory exists
    os.makedirs(static_dir, exist_ok=True)

    # File path in the static folder
    file_path = os.path.join(static_dir, file.name)
    

    # Save the file
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    try:
        # Read the CSV file instead of Excel
        df = pd.read_csv(file_path)

        # Ensure only the required columns are processed
        df = df[list(required_fields.keys())]

        entries = []

        # Validate and clean data
        for index, row in df.iterrows():
            cleaned_row = validate_and_clean_row(row)
            entries.append(Company_Data(
                Name=cleaned_row['Name'],
                Domain=cleaned_row['Domain'],
                YearFounded=cleaned_row['YearFounded'],
                Industry=cleaned_row['Industry'],
                City=cleaned_row['City'],
                State=cleaned_row['State'],
                Country=cleaned_row['Country'],
                LinkedinUrl=cleaned_row['LinkedinUrl']
            ))

        # Remove the temporary file
        os.remove(file_path)
        # print("entries--",entries)
        # Bulk create records
        with transaction.atomic():
            
            Company_Data.objects.bulk_create(entries)

    except pd.errors.ParserError as e:
        print(f"Error reading CSV file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")