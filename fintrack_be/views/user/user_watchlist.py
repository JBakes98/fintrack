from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from fintrack_be.models import User
from fintrack_be.serializers import UserWatchlistSerializer


class UserWatchlistAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserWatchlistSerializer
    queryset = User.objects.all()

    def get(self, request):
        """
        Method for to get tokens users favourites watchlist
        """
        serializer = self.serializer_class(self.request.user)
        return Response(serializer.data)
