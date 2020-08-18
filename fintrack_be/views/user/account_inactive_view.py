from rest_framework.response import Response
from rest_framework.views import APIView


class AccountInactiveView(APIView):
    def get(self, *args, **kwargs):
        return Response({'detail': 'User account is not active'})

    def post(self, *args, **kwargs):
        return Response({'detail': 'User account is not active'})