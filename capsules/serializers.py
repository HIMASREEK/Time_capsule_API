from rest_framework import serializers
from .models import Capsule

class CapsuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Capsule
        fields = '__all__'
        read_only_fields = ['user', 'is_opened']