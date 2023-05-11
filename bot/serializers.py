from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from bot.models import TgUser


class TgUserSerializer(serializers.ModelSerializer):
    tg_id = serializers.SlugField(source='chat_id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = TgUser
        fields = ('tg_id', 'username', 'verification_code', 'user_id')
        read_only_fields = ('tg_id', 'username', 'user_id')
        extra_kwargs = {'verification_code':{'write_only': True}}