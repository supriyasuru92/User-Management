from django.db import models
from django.contrib.auth.models import User


GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)
MARITAL_STATUS_CHOICES = (
    ('Single', 'Single'),
    ('Married', 'Married'),
    ('Divorcee', 'Divorcee'),
    ('Widow', 'Widow'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    designation = models.CharField(max_length=150, blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    postal_code = models.PositiveIntegerField(blank=True, null=True)
    locality = models.CharField(max_length=30, blank=True, null=True)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, blank=True, null=True)
    photo = models.ImageField(default='default.jpg', upload_to='profile_images', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


