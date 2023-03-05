from django.contrib.auth.models import User
from rest_framework import serializers

from user.models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

        def create(self, validated_data):
            user = User.objects.create(username=validated_data['username'], email=validated_data['email'],
                                       first_name=validated_data['first_name'], last_name=validated_data['last_name'])
            user.set_password(validated_data['password'])
            user.save()
            return user


class AllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['birth_date', 'gender', 'designation', 'address', 'postal_code', 'locality', 'marital_status', 'photo'
            , 'bio']
