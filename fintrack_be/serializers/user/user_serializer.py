from rest_framework import serializers
from fintrack_be.models import User
from fintrack_be.models import Country


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
