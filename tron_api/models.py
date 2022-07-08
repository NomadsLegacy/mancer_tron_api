from django.db import models

class Wallet(models.Model):
    email_address = models.CharField(max_length=200)
    password = models.CharField(max_length=100)
    wallet_address = models.CharField(max_length=500)
    private_key = models.CharField(max_length=500)
    amount = models.CharField(max_length=100)