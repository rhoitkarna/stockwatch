from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'email', 
            'full_name', 
            'password', 
            'password_confirm', 
            'account_tier', 
            'timezone', 
            'preferred_currency'
        ]

    def validate(self, attrs):
        # 1. Check if passwords match
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # 2. Prevent users from registering themselves as ADMIN via API
        if attrs.get('account_tier') == User.AccountTier.ADMIN:
            raise serializers.ValidationError({"account_tier": "Cannot register as ADMIN tier through this endpoint."})
            
        return attrs

    def create(self, validated_data):
        # Remove password_confirm before passing to the manager
        validated_data.pop('password_confirm')
        
        # This calls your UserManager.create_user() which handles set_password()
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing and updating user profile data.
    Notice 'id' (UUID) is read-only by default as a primary key.
    """
    class Meta:
        model = User
        fields = [
            'id', 
            'email', 
            'full_name', 
            'account_tier', 
            'timezone', 
            'preferred_currency',
            'last_login'
        ]
        # These fields should not be editable by the user directly in a profile update
        read_only_fields = ['id', 'email', 'account_tier', 'last_login']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)