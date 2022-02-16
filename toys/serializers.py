
from rest_framework import serializers
from toys.models import Toy


class ToySerializer(serializers.ModelSerializer):
    """Serializer for the toy object. May have to come back to book page 43"""

    class Meta:
        model = Toy
        fields = "__all__"
        read_only_fields = ("id",)
