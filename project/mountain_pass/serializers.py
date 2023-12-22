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
    level = LevelSerializer(allow_null=True)
    images = ImageSerializer(many=True)

    class Meta:
        model = Pereval
        fields = ['status', 'beauty_title', 'title', 'other_title', 'connect', 'add_time', 'user', 'coords', 'level',
                  'images']

    def create(self, validated_data, **kwargs):
        user = validated_data.pop('user')
        coords = validated_data.pop('coords')
        level = validated_data.pop('level')
        images = validated_data.pop('images')

        user, created = AppUser.objects.get_or_create(**user)

        coords = Coords.objects.create(**coords)
        level = Level.objects.create(**level)
        pereval = Pereval.objects.create(**validated_data, user=user, coords=coords, level=level)

        for im in images:
            image = im.pop('image')
            title = im.pop('title')
            Image.objects.create(title=title, image=image, perval=pereval)
        return pereval

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


