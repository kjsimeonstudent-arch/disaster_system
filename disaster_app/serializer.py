from rest_framework import serializers
from .models import User, Disaster, Request, Report
import hashlib


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'password', 'role', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if password is not None:
            # store hashed password
            validated_data['password'] = hashlib.sha256(password.encode()).hexdigest()
        return super().create(validated_data)


class DisasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disaster
        fields = ['id', 'type', 'message', 'location', 'severity', 'timestamp']
        read_only_fields = ['timestamp']


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['id', 'user', 'type', 'description', 'location', 'is_sos', 'status', 'timestamp', 'form_id', 'source_page']
        read_only_fields = ['timestamp']


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'user', 'type', 'description', 'location', 'status', 'timestamp', 'form_id', 'source_page']
        read_only_fields = ['timestamp']