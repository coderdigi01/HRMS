from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
import random

class UserManager(BaseUserManager):
    def create_user(self, mobile_number, password=None):
        if not mobile_number:
            raise ValueError("Users must have a mobile number")
        user = self.model(mobile_number=mobile_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, password=None):
        user = self.create_user(mobile_number, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class UserProfile(AbstractBaseUser):
    mobile_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.mobile_number

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class OTP(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP for {self.user.mobile_number} - {self.otp}"

    # Check if OTP is still valid (e.g., valid for 5 minutes)
    def is_valid(self):
        now = timezone.now()
        return (now - self.created_at).seconds < 300  # OTP is valid for 5 minutes

    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))