from typing import Any
from rest_framework import generics, permissions
from rest_framework.exceptions import AuthenticationFailed
from bot.serializers import TgUserSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from bot.models import TgUser



class VerificationCodeView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializers_class = TgUserSerializer

    def patch(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer: TgUserSerializer = self.get_serializer(data=request.data)
        serializer. is_valid(raise_exeption=True)
        try:
            tg_user = TgUser.objects.get(verification_code=serializer.validated_data['verification_code'])
        except TgUser.DoesNotExist:
            raise AuthenticationFailed

        tg_user.user = request.user
        tg_user.save()
        TgClient().send_message(chat_id=tg_user.chat_id, text='Bot has been verified')

        return Response(TgUserSerializer(tg_user).data)