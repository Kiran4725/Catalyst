from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from Count_App.models import *
from Count_App.serializers import *
from Count_App.methods import *
from rest_framework import status
from django.db import transaction
import os
from django.conf import settings
import csv
import pandas as pd
import json
import string, random

from django.db.models import Min, Max
from django.db.models import Q


baseURL = "http://127.0.0.1:8000/"


def login(request):
    try:
        if request.method == 'POST':
            char_set = string.ascii_uppercase + string.digits
            session_key = ''.join(random.sample(char_set * 20, 20))

            data = json.loads(request.body.decode('utf-8'))
            
            email_id = data.get('email')
            password = data.get('password')

            # Check if a user with the given email exists
            user = list(User.objects.filter(Q(Email=email_id) & Q(Password=password)))
            if len(user) == 0:
                context_data = {'status': False,'message': 'Invalid email or password !'}
            else:
                request.session['name'] = user[0].FullName
                request.session['session_key'] = session_key
                context_data = {'status': True,'message': 'Login successful !'}

            return HttpResponse(json.dumps(context_data, default=str), content_type="application/json")
        elif request.method == 'GET':
            return render(request,"login.html",{'baseURL':baseURL})
    except Exception as e:
        context_data = {'message': 'login page not responding proper please try later !','status': False}
        return HttpResponse(json.dumps(context_data, default=str), content_type="application/json")


def registration(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            
            name = data.get('name')
            email= data.get('email')
            contact = data.get('contact')
            password = data.get('password')

            user_data = {
                'FullName': name,
                'Email': email,
                'PhoneNo': contact,
                'Password': password
            }
            
            # Use the serializer to validate and save the data
            serializer = UserSerializer(data=user_data)
            
            if serializer.is_valid():
                serializer.save()
                context_data = {'message': 'Registration successful!', 'status': True}
            else:
                context_data = {'message': 'Invalid data!', 'status': False, 'errors': serializer.errors}
                
            return HttpResponse(json.dumps(context_data, default=str), content_type="application/json")
            
        elif request.method == 'GET':
            return render(request,"register.html",{'baseURL':baseURL})
    except Exception as e:
        context_data = {'message': 'Registration page not responding proper please try later !','status': False}
        return HttpResponse(json.dumps(context_data, default=str), content_type="application/json")
    

def upload_data(request):
    if request.session.has_key('session_key'):
        try:
            if request.method == 'POST':
                file = request.FILES.get('file')
                if file:
                    Company_Data.objects.all().delete()
                    process_csv(file)
                    context_data = {'message': 'Data Upload successfully !', 'status': True}
                    return HttpResponse(json.dumps(context_data, default=str), content_type="application/json")
            elif request.method == 'GET':
                return render(request,"upload_data.html",{'baseURL':baseURL})
        except Exception as e:
            context_data = {'message': 'Upload data page not responding proper please try later !','status': False}
            return HttpResponse(json.dumps(context_data, default=str), content_type="application/json")
    else:
        return redirect(baseURL)   
    

def query_builder(request):
    if request.session.has_key('session_key'):
        try:
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))

                company_name = data.get('company_name', '')
                industry = data.get('industry', '')
                city = data.get('city', '')
                state = data.get('state', '')
                country = data.get('country', '')
                year_founded = str(data.get('year_founded', ''))

                # Build the query with filters
                filter_kwargs = {}
                if company_name:
                    filter_kwargs['Name__icontains'] = company_name
                if industry:
                    filter_kwargs['Industry__icontains'] = industry
                if city:
                    filter_kwargs['City__icontains'] = city
                if state:
                    filter_kwargs['State__icontains'] = state
                if country:
                    filter_kwargs['Country__icontains'] = country
                if year_founded:
                    filter_kwargs['YearFounded'] = year_founded


                # Apply filters to the queryset
                companies = Company_Data.objects.filter(**filter_kwargs)
                
                count = companies.count()
                
                context_data = {'message': f'{count} records found for the query !', 'status': True}
                return HttpResponse(json.dumps(context_data, default=str), content_type="application/json")
                
            elif request.method == 'GET':
                industry_list = Company_Data.objects.filter(~Q(Industry='')).values_list('Industry', flat=True).distinct()
                city_list = Company_Data.objects.filter(~Q(City='')).values_list('City', flat=True).distinct()
                state_list = Company_Data.objects.filter(~Q(State='')).values_list('State', flat=True).distinct()
                country_list = Company_Data.objects.filter(~Q(Country='')).values_list('Country', flat=True).distinct()

                # Get minimum and maximum YearFounded, excluding 0 for the minimum
                year_founded = Company_Data.objects.aggregate(
                    min_year=Min('YearFounded', filter=~Q(YearFounded='0')),
                    max_year=Max('YearFounded')
                )
                min_year_founded = int(year_founded['min_year'])
                max_year_founded =  int(year_founded['max_year'])

            
                return render(request,"query_builder.html",
                              {'baseURL':baseURL,'industry_list':industry_list,'city_list':city_list,
                               'state_list':state_list,'country_list':country_list,'min_year_founded':min_year_founded,
                               'max_year_founded':max_year_founded})
        except Exception as e:
            context_data = {'message': 'Query Builder page not responding proper please try later !','status': False}
            return HttpResponse(json.dumps(context_data, default=str), content_type="application/json") 
    else:
        return redirect(baseURL)   
    

def users(request):
    if request.session.has_key('session_key'):
        try:
            if request.method == 'GET':
                user_data = User.objects.all()
                user_ser = UserSerializer(user_data, many=True)
                return render(request,"users.html",{'baseURL':baseURL,'data':user_ser.data})
        except Exception as e:
            context_data = {'message': 'Users page not responding proper please try later !','status': False}
            return HttpResponse(json.dumps(context_data, default=str), content_type="application/json")  
    else:
        return redirect(baseURL) 


def logout(request):
    try:
        del request.session['session_key']
        return redirect(baseURL)
    except KeyError:
        return redirect(baseURL) 
    
