from rest_framework import serializers
from .models import dev_data

class Wallet_serializers(serializers.ModelSerializer):
    class Meta:
        model = dev_data
        fields =['wallet_address','private_key','TitleId']