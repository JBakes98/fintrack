from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from stock.serializers import StockWatchlistSerializer

UserModel = get_user_model()


class UserWatchlistAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = StockWatchlistSerializer
    UserModel.objects.all()

    def get(self, request):
        """
        Method for to get tokens users favourites watchlist
        """
        serializer = self.serializer_class(self.request.user)
        return Response(serializer.data)