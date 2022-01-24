from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Location

from job.serializers import LocationSerializer


LOCATIONS_URL = reverse('job:location-list')


class PublicLocationApiTests(TestCase):
    """Test the publicly available locations API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required for retrieving locations"""
        res = self.client.get(LOCATIONS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateLocationApiTests(TestCase):
    """Test the authorized user locations API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@appdev.com',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_location(self):
        """Test retrieving locations"""
        Location.objects.create(user=self.user, state = 'MA', city = 'Boston',
                            street_address = 'test',
                            remote = 'fr')
        Location.objects.create(user=self.user, state = 'CA', city = 'Irvine',
                            street_address = 'test2',
                            remote = 'fr')
        res = self.client.get(LOCATIONS_URL)

        locations = Location.objects.all().order_by('-id')
        serializer = LocationSerializer(locations, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_location_limited_to_user(self):
        """Test that locations returned are for authenticated user"""
        user2 = get_user_model().objects.create_user(
            'other@appdev.com',
            'testpass'
        )
        Location.objects.create(user=user2, state = 'MA', city = 'Boston',
                                street_address = 'test',
                                remote = 'fr')
        location = Location.objects.create(user=self.user, state = 'CA', city = 'Irvine',
                                street_address = 'test2',
                                remote = 'fr')
        res = self.client.get(LOCATIONS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['state'], location.state)

    def test_create_location_successful(self):
        """Test creating a new location"""
        payload = {'state' : 'MA', 'city' : 'Boston',
                    'street_address' : 'test', 'remote' : 'fr'}
        self.client.post(LOCATIONS_URL, payload)

        exists = Location.objects.filter(
            user = self.user,
            city = payload['city']
        ).exists()
        self.assertTrue(exists)

    def test_create_location_invalid(self):
        """Test creating a new location with invalid payload"""
        payload = {'state': ''}
        res = self.client.post(LOCATIONS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
