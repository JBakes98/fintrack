from rest_framework import serializers
from fintrack_be.models import User
from fintrack_be.models import Country


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    country = serializers.SlugRelatedField(queryset=Country.objects.all(), slug_field='alpha2')

    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'email',
                  'password',
                  'password2',
                  'country',
                  'is_verified',
                  'is_active',
                  'funds',
                  'value',
                  'result')
        depth = 1
        read_only_fields = ('is_verified', )

    def create(self, validated_data):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password', 'Passwords must match'})

        user = User.objects.create_user(
            email=self.validated_data['email'],
            password=password,
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            country=self.validated_data['country'],
        )

        return user
