from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import IsVerified
from stock.models import Stock

UserModel = get_user_model()


class WatchStockView(APIView):
    permission_classes = (IsAuthenticated, IsVerified)

    def post(self, request, ticker):
        try:
            stock = Stock.objects.get(ticker=ticker)
        except Stock.DoesNotExist:
            return Response({'detail': 'Stock with ticker {} not found'.format(ticker)})

        user = request.user
        if Stock.objects.filter(pk=stock.pk, watchlist=user):
            stock.watchlist.remove(user)
            return Response({"detail": '{} Removed from watchlist'.format(ticker)})
        else:
            stock.watchlist.add(user)
            return Response({'detail': '{} Added to watchlist'.format(ticker)})
