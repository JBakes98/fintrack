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

    def save(self):
        data = self.validated_data
        print(type(data))
        return PositionService.open_position(self.context['request'].user, self.validated_data)
