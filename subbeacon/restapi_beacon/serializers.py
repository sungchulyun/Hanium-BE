from rest_framework import serializers
from restapi_beacon.models import User, ocrimg, subway, arrival, destination, subwayim, userstatus, naviroot



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('userid', 'userpw',)


class subwaySerializer(serializers.ModelSerializer):
    class Meta:
        model = subway
        fields = ('subwaynum', 'subwaysta',)

class arrivalSerializer(serializers.ModelSerializer):
    class Meta:
        model = arrival
        fields = ('station', 'trainline', 'arrivetime', 'trainnum')

class destinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = destination
        fields = ('startdet', 'enddet')

class subwayimSerializer(serializers.ModelSerializer):
    class Meta:
        model = subwayim
        fields = ('substa', 'subid')

class userstatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = userstatus
        fields = ('usersta', 'usertrain')

class navirootSerializer(serializers.ModelSerializer):
    class Meta:
        model = naviroot
        fields = ('startline', 'startwname', 'startwcode', 'exchaline', 'exchawname', 'exchawcode')

class ocrimgSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    
    class Meta:
        model = ocrimg
        fields = ('title', 'image')