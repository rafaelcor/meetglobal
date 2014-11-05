from django.db import models
from django.contrib.auth.models import User as DjangoUser
# Create your models here.

class User(models.Model):
    dateOfBirth = models.DateField()
    dateOfBirth.contribute_to_class(DjangoUser, 'date_of_birth')
    email = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    auth_user = models.ForeignKey(DjangoUser)
    password = models.CharField(max_length=200)
    languages = models.CharField(max_length=200)
    image = models.ImageField(upload_to="/page/static/page/media")
    messagesNotRead = models.IntegerField()
    

class UsersToConfirm(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    dateOfBirth = models.DateField()
    email = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    password = models.CharField(max_length=200)
    random_link_subfix = models.CharField(max_length=200)


class Message(models.Model):
    sender = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)
    message = models.CharField(max_length=500)
    read = models.BooleanField(default=False)


class Document(models.Model):
    filename = models.CharField(max_length=100)
    docfile = models.FileField(upload_to='imgProfiles/')


country = models.CharField(max_length=100)
country.contribute_to_class(DjangoUser, 'country')

language = models.CharField(max_length=100)
language.contribute_to_class(DjangoUser, 'language')

image = models.ImageField(upload_to="/media")
image.contribute_to_class(DjangoUser, 'image')
