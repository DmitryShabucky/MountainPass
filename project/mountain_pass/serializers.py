from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from .models import Pereval, AppUser, Coords, Level, Image


class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['email', 'fam', 'name', 'otc', 'phone']

class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['winter', 'summer', 'autumn', 'spring']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['title', 'image']

class PerevalSerializer(WritableNestedModelSerializer):
    status = serializers.CharField(read_only=True)
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    user = AppUserSerializer()
    coords = CoordsSerializer()
    level = LevelSerializer()
    images = ImageSerializer(many=True)

    def validate(self, value):

        user_data = value['user']

        if self.instance:
            if (user_data['email'] != self.instance.user.email or
                    user_data['fam'] != self.instance.user.fam or
                    user_data['name'] != self.instance.user.name or
                    user_data['otc'] != self.instance.user.otc or
                    user_data['phone'] != self.instance.user.phone):
                raise serializers.ValidationError()
        return value

    class Meta:
        model = Pereval
        fields = ['status', 'beauty_title', 'title', 'other_title', 'connect', 'add_time', 'user', 'coords', 'level',
                  'images']
