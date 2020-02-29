from rest_framework import serializers
from users.serializers import RelatedUserSerializer
from .models import Room

class ReadRoomSerializer(serializers.ModelSerializer):

    user = RelatedUserSerializer()

    class Meta:
        model = Room
        exclude = ("modified",)

class WriteRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        exclude = ("user", "modified", "created")

    def validate(self, data):
        #instance가 존재하지 않는다는 것은 객체를 새로 만드는 상황을 의미
        if self.instance:
            check_in = data.get("check_in", self.instance.check_in)
            check_out = data.get("check_out", self.instance.check_out)
        else:
            check_in = data.get("check_in")
            check_out = data.get("check_out")

        if check_in == check_out:
            raise serializers.ValidationError("Not enough time between changes")
        return data

