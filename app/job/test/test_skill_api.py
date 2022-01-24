from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Skill

from job.serializers import SkillSerializer


SKILLS_URL = reverse('job:skill-list')


class PublicSkillApiTests(TestCase):
    """Test the publicly available skill API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required for retrieving skills"""
        res = self.client.get(SKILLS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateSkillApiTests(TestCase):
    """Test the authorized user skill API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@appdev.com',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_skill(self):
        """Test retrieving skills"""
        #{'id','skill', 'skill_level'}
        Skill.objects.create(user=self.user, skill = 'c++', skill_level = 'good')
        Skill.objects.create(user=self.user, skill = 'python', skill_level = 'good')
        res = self.client.get(SKILLS_URL)

        skills = Skill.objects.all().order_by('-id')
        serializer = SkillSerializer(skills, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_skill_limited_to_user(self):
        """Test that skills returned are for authenticated user"""
        user2 = get_user_model().objects.create_user(
            'other@appdev.com',
            'testpass'
        )
        Skill.objects.create(user=user2, skill = 'c++', skill_level = 'good')
        skill = Skill.objects.create(user=self.user, skill = 'python', skill_level = 'good')
        res = self.client.get(SKILLS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['skill'], skill.skill)

    def test_create_skill_successful(self):
        """Test creating a new skill"""
        payload = {'skill' : 'c', 'skill_level' : 'good'}
        self.client.post(SKILLS_URL, payload)

        exists = Skill.objects.filter(
            user = self.user,
            skill = payload['skill']
        ).exists()
        self.assertTrue(exists)

    def test_create_skill_invalid(self):
        """Test creating a new skill with invalid payload"""
        payload = {'skill': ''}
        res = self.client.post(SKILLS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
