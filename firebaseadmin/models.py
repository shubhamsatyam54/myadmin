from django.db import models

# Create your models here.
from django.db import models

class Account(models.Model):
    email = models.EmailField(unique=True)  # Email should be unique for each account
    password = models.CharField(max_length=128)  # Password length, adjusted as needed

    def __str__(self):
        return self.email

class Subscription(models.Model):

    account = models.ForeignKey(Account, on_delete=models.CASCADE, to_field='email', related_name='subscriptions')
    vehicle = models.CharField(max_length=100)  # Vehicle identifier
    subscription = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.account.email} - {self.vehicle} - {self.subscription}"
