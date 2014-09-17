from django.db import models
from django.contrib.auth.models import User as DjangoUser
# Create your models here.

class User(models.Model):
    email = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    auth_user = models.ForeignKey(DjangoUser)
    password = models.CharField(max_length=200)
    languages = models.CharField(max_length=200)


class UsersToConfirm(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    password = models.CharField(max_length=200)
    random_link_subfix = models.CharField(max_length=200)

country = models.CharField(max_length=100)
country.contribute_to_class(DjangoUser, 'country')

language = models.CharField(max_length=100)
language.contribute_to_class(DjangoUser, 'language')