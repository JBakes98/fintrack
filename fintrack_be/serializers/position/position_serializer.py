from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from fintrack_be.models import User, Stock, Position
from fintrack_be.services.position.position_services import PositionService


class PositionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    open_date = serializers.DateTimeField(required=False)
    instrument = serializers.SlugRelatedField(queryset=Stock.objects.all(), slug_field='ticker')

    class Meta:
        model = Position
        fields = ['id', 'instrument', 'user', 'open_date', 'close_date', 'open_price', 'close_price',
                  'quantity', 'result', 'direction']


class PositionCloseSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    close_date = serializers.DateTimeField(required=False)
    instrument = serializers.SlugRelatedField(read_only=True, slug_field='ticker')

    class Meta:
        model = Position
        fields = ['id', 'instrument', 'user', 'open_date', 'close_date', 'open_price', 'close_price',
                  'quantity', 'result', 'direction']
        read_only_fields = ('id', 'instrument', 'user', 'open_date', 'open_price', 'quantity', 'direction')
