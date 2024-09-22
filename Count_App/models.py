from django.db import models

# Create your models here.

class User(models.Model):
    Id = models.AutoField(primary_key=True)
    FullName = models.CharField(max_length=255)
    Email = models.EmailField(max_length=255)
    Password = models.CharField(max_length=255)
    PhoneNo = models.CharField(max_length=12)


    class Meta:
        db_table = 'User'
        managed = False


class Company_Data(models.Model):
    Id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    Domain = models.CharField(max_length=225)
    YearFounded = models.CharField(max_length=225)
    Industry = models.CharField(max_length=225)
    City = models.CharField(max_length=225)
    State = models.CharField(max_length=225)
    Country = models.CharField(max_length=225)
    LinkedinUrl = models.CharField(max_length=225)

    class Meta:
        db_table = 'Company_Data'
        managed = True