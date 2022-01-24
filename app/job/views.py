from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Skill
from core.models import Location
from core.models import Job
# from core.models import Job
from job import serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
# from job import serializers

# class TagViewSet(viewsets.GenericViewSet,
#                  mixins.ListModelMixin,
#                  mixins.CreateModelMixin):
#     """Manage tags in the database"""
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     queryset = Tag.objects.all()
#     serializer_class = serializers.TagSerializer
#
#     def get_queryset(self):
#         """Return objects for current authenticated user only"""
#         return self.queryset.filter(user=self.request.user).order_by('-name')
#
#     def perform_create(self, serializer):
#         """Create a new tag"""
#         serializer.save(user = self.request.user)

class SkillViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """Manage tags in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Skill.objects.all()
    serializer_class = serializers.SkillSerializer

    def get_queryset(self):
        """Return objects for current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new tag"""
        serializer.save(user = self.request.user)

class LocationViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """Manage tags in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Location.objects.all()
    serializer_class = serializers.LocationSerializer

    def get_queryset(self):
        """Return objects for current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new tag"""
        serializer.save(user = self.request.user)

class JobViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """Manage tags in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Job.objects.all()
    serializer_class = serializers.JobSerializer

    def get_queryset(self):
        """Return objects for current authenticated user only"""
        filter_backends = [filters.SearchFilter, DjangoFilterBackend]
        search_fields = ['job_title']
        filterset_fields = ['experience', 'sponsorship']
        return self.queryset.filter(user=self.request.user) #.order_by('-name')

    def perform_create(self, serializer):
        """Create a new job info post"""
        serializer.save(user = self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.JobDetailSerializer

        return self.serializer_class
