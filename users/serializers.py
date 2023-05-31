from rest_framework import serializers

from users.models import User


class RelatedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            'user_permissions', 'groups', 'password', 'superhost', 'is_superuser', 'is_staff', 'is_active', 'last_name',
            'favs', 'date_joined',)




class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'last_login',
            'username',
            'first_name',
            'email',
            'avatar',
            'password',
        )
        read_only_fields = ('id', 'last_login', 'avatar')

    def create(self, validated_data):
        password = validated_data.get('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user