from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Job, Skill, Location

from job.serializers import JobSerializer, JobDetailSerializer


JOBS_URL = reverse('job:job-list')

def sample_job(user, **params):
    """Create and return a sample job"""
    #'id', 'job_title', 'skill', 'location', 'description','time', 'sponsorship', 'experience', 'company'
    defaults = {
        'job_title' : 'Software Engineer',
        'sponsorship' : 'y',
        'description' : 'I believe I deserve an offer',
        'time' : 20220112,
        'experience' : 'year0',
        'company' : 'Netflix'
    }
    defaults.update(params)

    return Job.objects.create(user=user, **defaults)

def detail_url(job_id):
    """Return job detail URL"""
    return reverse('job:job-detail', args=[job_id])


def sample_skill(user):
    """Create and return a sample skill"""
    return Skill.objects.create(user=user,skill = 'c++', skill_level = 'good')


def sample_location(user):
    """Create and return a sample location"""
    return Location.objects.create(user=user, state = 'CA', city = 'Irvine',
                            street_address = 'test2',
                            remote = 'fr')


class PublicJobApiTests(TestCase):
    """Test unauthenticated job API access"""

    def setUp(self):
        self.client = APIClient()

    def test_required_auth(self):
        """Test the authenticaiton is required"""
        res = self.client.get(JOBS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateJobApiTests(TestCase):
    """Test authenticated job API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@appdev.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_job(self):
        """Test retrieving list of jobs"""
        sample_job(user=self.user)
        sample_job(user=self.user)

        res = self.client.get(JOBS_URL)

        jobs = Job.objects.all().order_by('-id')
        serializer = JobSerializer(jobs, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_job_limited_to_user(self):
        """Test retrieving jobs for user"""
        user2 = get_user_model().objects.create_user(
            'other@londonappdev.com',
            'password123'
        )
        sample_job(user=user2)
        sample_job(user=self.user)

        res = self.client.get(JOBS_URL)

        jobs = Job.objects.filter(user=self.user)
        serializer = JobSerializer(jobs, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_job_detail(self):
        """Test viewing a job detail"""
        job = sample_job(user=self.user)
        job.skill.add(sample_skill(user=self.user))
        job.location.add(sample_location(user=self.user))

        url = detail_url(job.id)
        res = self.client.get(url)

        serializer = JobDetailSerializer(job)
        self.assertEqual(res.data, serializer.data)

    def test_create_job_with_skill(self):
    """Test creating a job with skills"""
        skill1 = sample_tag(user=self.user, skill = 'c++', skill_level = 'good')
        skill2 = sample_tag(user=self.user, skill = 'c', skill_level = 'good')
        payload = {
            'job_title': 'swe',
            'tags': [skill1.id, skill2.id],
            'time': 60,
            'experience': 'year0',
            'company' : 'Netflix',
            'sponsorship' : 'y',
            'description' : 'spring coming',
        }
        res = self.client.post(JOBS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        job = Job.objects.get(id=res.data['id'])
        skills = job.skill.all()
        self.assertEqual(skills.count(), 2)
        self.assertIn(skill1, skills)
        self.assertIn(skill2, skills)
