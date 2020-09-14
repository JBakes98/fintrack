from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django.utils.translation import ugettext_lazy as _

from account.serializers import AccountVerificationSerializer


class AccountVerifyConfirmView(GenericAPIView):
    """
    Password reset e-mail link is confirmed, therefore
    this resets the user's password.

    Accepts the following POST parameters: token, uid,
        new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = AccountVerificationSerializer
    permission_classes = (AllowAny,)

    def dispatch(self, *args, **kwargs):
        return super(AccountVerifyConfirmView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=kwargs)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": _("Thank you for verifying your account.")}
        )