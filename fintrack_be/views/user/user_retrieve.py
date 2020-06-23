from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from fintrack_be.serializers import UserSerializer


class UserDetailAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = self.request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)