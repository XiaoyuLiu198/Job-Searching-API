from django.urls import path, include
from rest_framework.routers import DefaultRouter
from job import views

router = DefaultRouter()
router.register('skill', views.SkillViewSet)
router.register('location', views.LocationViewSet)
router.register('job', views.JobViewSet)
router.register('job-detail', views.JobViewSet)

app_name = 'job'

urlpatterns = [
    path('', include(router.urls))
]
