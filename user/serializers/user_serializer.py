from rest_framework import serializers
from user.models import User
from country.models import Country


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    country = serializers.SlugRelatedField(queryset=Country.objects.all(), slug_field='alpha2')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'country', 'is_verified', 'favourite_stocks')
        depth = 1
        read_only_fields = ('is_verified', )

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user


class SuperUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    country = serializers.SlugRelatedField(queryset=Country.objects.all(), slug_field='alpha2')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'country', 'is_superuser', 'is_staff']

    def create(self, validated_data):
        user = super(SuperUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user


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
