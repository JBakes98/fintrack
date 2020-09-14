from rest_framework.response import Response
from rest_framework.views import APIView


class AccountEmailVerificationSentView(APIView):
    def get(self, *args, **kwargs):
        return Response({'detail': 'Account email verification sent'})

    def post(self, *args, **kwargs):
        return Response({'detail': 'Account email verification sent'})