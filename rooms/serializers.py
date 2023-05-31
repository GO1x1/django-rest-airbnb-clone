from rest_framework import serializers

from rooms.models import Room
from users.serializers import RelatedUserSerializer


class RoomSerializer(serializers.ModelSerializer):
    user = RelatedUserSerializer(read_only=True)
    is_fav = serializers.SerializerMethodField()

    class Meta:
        model = Room
        exclude = ('modified',)
        read_only_fields = ('user', 'created', 'updated')

    def create(self, validated_data):
        request = self.context.get('request')
        room = Room.objects.create(**validated_data, user=request.user)
        return room

    def get_is_fav(self, obj):
        request = self.context.get('request')
        if request:
            if request.user.is_authenticated:
                return obj in request.user.favs.all()
        else:
            return False
