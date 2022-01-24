from rest_framework import serializers
from core.models import Job, Skill, Location

# class TagSerializer(serializers.ModelSerializer):
#     """Serializer for job objects"""
#
#     class Meta:
#         model = Tag
#         fields = {'id','name'}
#         read_only_fields = {'id',}
#skillset and location
class SkillSerializer(serializers.ModelSerializer):
    """Serializer for skill objects"""

    class Meta:
        model = Skill
        fields = ('id','skill', 'skill_level')
        read_only_fields = ('id',)

class LocationSerializer(serializers.ModelSerializer):
    """Serializer for location objects"""
    class Meta:
        model = Location
        fields = ('id', 'state', 'city', 'street_address', 'remote',)
        read_only_fields = ('id',)

# class FavoriteListSerializer(serializers.ModelSerializer):
#     owner = serializers.IntegerField(required=False)
#     class Meta:
#         model = models.FavoriteList
#
#     def get_validation_exclusions(self):
#         exclusions = super(FavoriteListSerializer, self).get_validation_exclusions()
#         return exclusions + ['owner']

# class RecipeSerializer(serializers.ModelSerializer):
#     ingredients = serializers.PrimaryKeyRelatedField(
#         many=True,
#         queryset=Ingredient.objects.all()
#     )
#     tags = serializers.PrimaryKeyRelatedField(
#         many=True,
#         queryset=Tag.objects.all()
#     )
#
#     class Meta:
#         model = Job
#         fields = (
#             'id', 'title', 'ingredients', 'tags', 'time_minutes',
#             'price', 'link'
#         )
#         read_only_fields = ('id',)

class JobSerializer(serializers.ModelSerializer):
    skill = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Skill.objects.all()
    )
    location = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Location.objects.all()
    )

    class Meta:
        model = Job
        fields = (
            'id', 'job_title', 'skill', 'location', 'description',
            'time', 'sponsorship', 'experience', 'company',
        )
        read_only_fields = ('id',)

class JobDetailSerializer(JobSerializer):
    """Serialize a job detail"""
    skill = SkillSerializer(many=True, read_only=True)
    location = LocationSerializer(many=True, read_only=True)
