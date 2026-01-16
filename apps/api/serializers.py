"""
API serializers.
"""
from rest_framework import serializers
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'full_name', 'phone', 'avatar', 'bio', 'date_of_birth',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new users."""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone'
        ]
    
    def validate(self, data):
        """Validate passwords match."""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Mật khẩu không khớp")
        return data
    
    def create(self, validated_data):
        """Create new user with encrypted password."""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user
