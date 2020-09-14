from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django.utils.translation import ugettext_lazy as _

from account.serializers import VerificationSerializer


class AccountVerifyConfirmView(GenericAPIView):
    """
    User Account is verified and the user can now use
    their account
    """
    serializer_class = VerificationSerializer
    permission_classes = (AllowAny,)

    def dispatch(self, *args, **kwargs):
        return super(AccountVerifyConfirmView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        # Can just pass kwargs to the serializer as this should contain both the uidb64 and
        # token values
        serializer = self.get_serializer(data=kwargs)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": _("Thank you for verifying your account.")}
        )
