from rest_framework import serializers

from apps.account.serializers_v1 import UserSerializer

from apps.chat.models import Message, Room


class MessageSerializer(serializers.ModelSerializer):
    created_at_formatted = serializers.SerializerMethodField()
    user = UserSerializer()

    class Meta:
        model = Message
        fields = ["room", "text", "user", "created_at_formatted"]
        depth = 1

    def get_created_at_formatted(self, obj):
        return obj.created_at.strftime("%d-%m-%Y %H:%M:%S")


class RoomSerializer(serializers.ModelSerializer):
    host = serializers.ReadOnlyField(source="host.email", read_only=True)
    last_message = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ["pk", "name", "host", "messages", "current_users", "last_message"]
        depth = 1

    def get_last_message(self, obj):
        last_message = obj.messages.order_by("created_at").last()
        if last_message:
            return MessageSerializer(last_message).data
        return None
