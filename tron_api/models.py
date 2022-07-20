from django.db import models

class dev_data(models.Model):
    wallet_address = models.CharField(max_length=100)
    private_key = models.CharField(max_length=200)
    TitleId = models.CharField(max_length=10)