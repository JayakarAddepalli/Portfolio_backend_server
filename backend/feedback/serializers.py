from rest_framework import serializers
from .models import FeedBackModel

class FeedBackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBackModel
        fields = '__all__'