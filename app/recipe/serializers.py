from rest_framework import serializers

from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe object"""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description')
        read_only_fields = ('id',)

    def create(self, validated_data):
        """Create a new recipe"""
        return Recipe.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.pop('name', None)
        instance.description = validated_data.pop('description', None)

        instance.save()
        return instance
