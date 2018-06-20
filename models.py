from django.db import models
# from app.storage import OverwriteStorage
# from django.conf import settings
import os
import datetime
from django.core.files.storage import FileSystemStorage
from .storage import OverwriteStorage

# Create your models here.
class Member(models.Model):
    account = models.CharField(max_length=30,null=False)
    password = models.CharField(max_length=30,null=False)
    useremail = models.EmailField(max_length=30,null=False)
    gender = models.CharField(max_length=5,null=False)
    userbirth = models.DateField(null=False)
    career = models.CharField(max_length=10,null=False)
    resident = models.CharField(max_length=5,null=False)

    
    class Meta:
        db_table = "members"

class Survey_Outcome(models.Model):
    account = models.CharField(max_length=30,null=False)
    Question1 = models.CharField(max_length=20,null=False)
    Question2 = models.CharField(max_length=20,null=False)
    Question3 = models.CharField(max_length=20,null=False)
    Question4 = models.CharField(max_length=20,null=False)
    Question5 = models.CharField(max_length=20,null=False)
    Question6 = models.CharField(max_length=20,null=False)
    Question6 = models.CharField(max_length=20,null=False)
    Question7 = models.CharField(max_length=200)

    class Meta:
        db_table = "survey_outcome"
    
class UserRecord(models.Model):
    account = models.CharField(max_length=30,null=False)
    Search_Record = models.CharField(max_length=50,null=False)
    # Satisfication = models.CharField(max_length=20,null=False)
    # login_time = models.CharField(max_length=20,null=False)
    # logout_time = models.CharField(max_length=20,null=False)

    class Meta:
        db_table = "UserRecord"


class PicSave(models.Model):
    pic = models.ImageField(max_length=128, storage=OverwriteStorage(), upload_to='pic/')