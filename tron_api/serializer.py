from rest_framework import serializers
from .models import Wallet

class Wallet_serializers(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields =['email_address','password','wallet_address','private_key','amount']