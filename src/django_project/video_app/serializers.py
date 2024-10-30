from rest_framework import serializers

from src.core.video.domain.value_objects import Rating


class RatingTypeField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        choices = [(type.name, type.value) for type in Rating]
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        return Rating(super().to_internal_value(data))

    def to_representation(self, value):
        return str(super().to_representation(value))


class SetField(serializers.ListField):
    def to_internal_value(self, data):
        return set(super().to_internal_value(data))

    def to_representation(self, value):
        return list(super().to_representation(value))


class CreateVideoWithoutMediaInputSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    launch_year = serializers.IntegerField()
    opened = serializers.BooleanField()
    duration = serializers.DecimalField(max_digits=5, decimal_places=2)
    rating = RatingTypeField(required=True)
    categories = SetField(child=serializers.UUIDField(), required=False)
    genres = SetField(child=serializers.UUIDField(), required=False)
    cast_members = SetField(child=serializers.UUIDField(), required=False)


class CreateVideoWithoutMediaOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
