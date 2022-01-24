from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        """Create user and save"""
        if not email:
            raise ValueError('Users must provide user email')
        user=self.model(email=self.normalize_email(email),**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password):
        user=self.create_user(email,password)
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user
class User(AbstractBaseUser,PermissionsMixin):
    """Custom user model that supports using email instead of username,by default it's only user name not email"""
    email=models.EmailField(max_length=255,unique=True)
    name=models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)

    objects=UserManager()

    USERNAME_FIELD='email'

# class Tag(models.Model):
#     """Tag to be used for a recipe"""
#     name = models.CharField(max_length = 255)
#     user = models.ForeignKey(
#     settings.AUTH_USER_MODEL,
#     on_delete=models.CASCADE,
#     )
#
#     def __str__(self):
#         return self.name

class Job(models.Model):
    """job"""
    # product = models.OneToOneField(
    #     Product,
    #     primary_key=True,
    #     on_delete=models.CASCADE
    # )
    job_title = models.CharField(max_length = 255)
    description = models.CharField(max_length = 2000)
    time = models.IntegerField()
    SPONSORSHIP_CHOICES = [
        ("y", 'Yes'),
        ("n", 'Only greencard holder or US Citizens'),
    ]
    sponsorship = models.CharField(
        max_length=2,
        choices=SPONSORSHIP_CHOICES,
        default="y",
    )
    # sponsorship = models.CharField(max_length = 255)
    EXPERIENCE_CHOICES = [
        ("year0", '<1 year'),
        ("year1", '1-3 years'),
        ("year2", '3-5 years'),
        ("year3", '>5 years'),
    ]
    experience = models.CharField(
        max_length=8,
        choices=EXPERIENCE_CHOICES,
        default="year0",
    )
    # experience = models.CharField(max_length = 255)
    company = models.CharField(max_length = 255)
    skill = models.ManyToManyField('Skill')
    location = models.ManyToManyField('Location')
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.job_title
class Skill(models.Model):
    """skill to be used for a job"""

    skill = models.CharField(max_length = 255)
    skill_level = models.CharField(max_length = 255)
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.skill
class Location(models.Model):
    """location to be used for a job"""
    #{'id', 'state', 'city', 'street_address', 'remote'}
    state = models.CharField(max_length = 255)
    city = models.CharField(max_length = 255)
    street_address = models.CharField(max_length = 255)
    REMOTE_CHOICES = [
        ("fr", 'Fully Remote'),
        ("po", '2-3 days in office'),
        ("os", 'on site'),
    ]
    remote = models.CharField(
        max_length=2,
        choices=REMOTE_CHOICES,
        default="fr",
    )
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.state
