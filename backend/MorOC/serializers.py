from rest_framework import serializers
from .models import BankOffer


class BankOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankOffer
        fields = "__all__"
