from rest_framework import serializers
from fintrack_be.models import User
from fintrack_be.models import Country


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    country = serializers.SlugRelatedField(queryset=Country.objects.all(), slug_field='alpha2')

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'country', 'password', 'password2']

    def create(self, validated_data):
        user = User(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            country=self.validated_data['country'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password', 'Passwords must match'})

        user.set_password(password)
        user.save()

        return user