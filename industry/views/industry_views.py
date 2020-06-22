from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from industry.models import Industry
from industry.serializers import IndustrySerializer, IndustryCompanySerializer
from fintrack.permissions import IsVerified


class IndustryViewSet(viewsets.ModelViewSet):
    """
        Industry ViewSet that offers the following actions, list(), retrieve(),
        create(), update(), partial_update() and destroy(). Depending on the
        HTTP method the User will require different permissions.

        The User must be Verified to use this method
        GET - List existing Industries or Retrieve specific Industry


        The User must be a Verified Admin User to use this methods
        POST - Create new Industry
        PUT - Fully update existing Industry
        PATCH - Partially update existing Industry
        DELETE - Delete existing Industry

        """
    serializer_class = IndustrySerializer
    lookup_field = 'name'

    def get_queryset(self):
        return Industry.objects.all()

    def get_permissions(self):
        request_method = self.request.method
        if request_method == 'GET':
            return (IsAuthenticated(), IsVerified())
        else:
            return (IsAdminUser(), IsVerified())


class IndustryCompanyListView(generics.ListAPIView):
    """
    Get an Industry instances Companies
    """
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = IndustryCompanySerializer
    queryset = Industry.objects.all()


class IndustryCompanyRetrieveView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = IndustryCompanySerializer

    def get_object(self):
        name = self.kwargs['name']
        return get_object_or_404(Industry, name=name)


# class IndustryStockListVIew(generics.ListAPIView):
#     """
#     Get a list of Stock instances in a Industry
#     """
#     permission_classes = (IsAuthenticated, IsVerified)
#     serializer_class = BasicStockSerializer
#
#     def get_queryset(self):
#         name = self.kwargs['name']
#         try:
#             industries = Industry.objects.filter(name=name)
#         except Industry.DoesNotExist:
#             raise Http404
#
#         try:
#             companies = Company.objects.filter(industry__in=industries)
#         except Company.DoesNotExist:
#             raise Http404
#
#         try:
#             stocks = Stock.objects.filter(company__in=companies).order_by('ticker')
#             latest_data = StockPriceData.objects.filter(stock=OuterRef('pk')).order_by('-timestamp')
#             return stocks.annotate(price=Subquery(latest_data.values('close')[:1]))
#         except Stock.DoesNotExist:
#             raise Http404
#         except StockPriceData.DoesNotExist:
#             raise Http404