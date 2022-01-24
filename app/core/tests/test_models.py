from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models

def sample_user(email = "jobsearchapi@gmail.com", password = 'testpswd'):
    return get_user_model().objects.create_user(email, password)

class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        email='test@xiaoyu.com'
        password="pswd123"
        user=get_user_model().objects.create_user(
        email=email,
        password=password
        )

        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """test the email of a new user is normalized"""
        email='test@xliu.com'
        user=get_user_model().objects.create_user(email,'test123')

        self.assertEqual(user.email,email.lower())

    def test_new_user_invalid_email(self):
        """test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None,'test123')

    def test_create_new_superuser(self):
        """test creating a new superuser"""
        user=get_user_model().objects.create_superuser(
        'test@xliu.com',
        'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_skill_str(self):
        """Test tag string representation"""
        #{'id','skill', 'skill_level'}
        skill = models.Skill.objects.create(
        user = sample_user(),
        skill = 'c++',
        skill_level = 'good'
        )

        self.assertEqual(str(skill), skill.skill)

    def test_location_str(self):
        """Test tag string representation"""
        #{'id', 'state', 'city', 'street_address', 'remote'}
        location = models.Location.objects.create(
        user = sample_user(),
        state = 'MA',
        city = 'Boston',
        street_address = 'test',
        remote = 'fr'
        )

        self.assertEqual(str(location), location.state)

    def test_job_str(self):
        """Test tag string representation"""
        #'id', 'job_title', 'skill', 'location', 'description','time', 'sponsorship', 'experience', 'company'
        job = models.Job.objects.create(
        user = sample_user(),
        job_title = 'swe',
        description = 'new grads',
        time = 20220112,
        sponsorship = 'y',
        experience = 'year0',
        company = 'Netflix'
        )

        self.assertEqual(str(job), job.job_title)
