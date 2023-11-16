from django.db import models
# This class provides a base implementation for user models with additional fields.
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import User


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_publisher = models.BooleanField(default=False)
    is_librarian = models.BooleanField(default=False)

    class Meta:
        # However in some cases, you might want to use your own custom user model, which is more flexible and can include additional fields.
        swappable = 'AUTH_USER_MODEl'


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    publisher = models.CharField(max_length=200)
    desc = models.CharField(max_length=1000)
    uploaded_by = models.CharField(max_length=100, null=True, blank=True)
    user_id = models.CharField(max_length=100, null=True, blank=True)
    pdf = models.FileField(upload_to='pdf')
    cover = models.ImageField(upload_to='covers', null=True, blank=True)
