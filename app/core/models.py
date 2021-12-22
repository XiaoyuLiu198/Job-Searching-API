from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
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
