from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone

Blood_Group_Choices = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
] 

Document_Choices= [
    ('Voter ID', 'Voter ID'),
    ('Passport ID', 'Passport ID'),
    ('Citizen ID', 'Citizen ID'),
]

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)

        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser = True")

        return self._create_user(email, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255 , blank=True, null=True)
    last_name = models.CharField(max_length=255 , blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True, help_text='Enter the date in the format: Y-M-D')
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    blood_group = models.CharField(max_length=3, null=True, blank=True, choices=Blood_Group_Choices)
    identity_document_type = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        choices=Document_Choices
    )
    identity_document_number = models.CharField(max_length=255, null=True, blank=True)
    photo = models.ImageField(null=True, upload_to='profile')
    date_joined = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name" ]

    objects = UserManager()
    
    def get_full_name(self):
        return f"{self.first_name}  {self.last_name}"
