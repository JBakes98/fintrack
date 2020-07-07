from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from fintrack_be.models import User
from fintrack_be.serializers import UserSerializer


class UserDetailsAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request):
        """
        Method for User to request an account verification email to be sent to
        the accounts email address to verify account.
        """
        serializer = self.serializer_class(self.request.user)
        return Response(serializer.data)
