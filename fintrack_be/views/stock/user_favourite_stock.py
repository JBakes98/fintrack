from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from fintrack_be.models import Stock, User
from fintrack_be.permissions import IsVerified


class UserFavouriteStockView(APIView):
    permission_classes = (IsAuthenticated, IsVerified)

    def post(self, request, ticker):
        try:
            stock = Stock.objects.get(ticker=ticker)
        except Stock.DoesNotExist:
            return Response('Stock with ticker {} not found'.format(ticker))

        user = request.user
        if User.objects.filter(pk=user.pk, favourite_stocks__pk=stock.pk):
            user.favourite_stocks.remove(stock)
            return Response('{} Removed from favourites'.format(ticker))
        else:
            user.favourite_stocks.add(stock)
            return Response('{} Added to favourites'.format(ticker))