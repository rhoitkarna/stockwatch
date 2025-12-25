from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email Required")
        
        email = self.normalize_email(email)
        user = self.model(email= email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
        

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)

    class AccountTier(models.TextChoices):
        ADMIN = "ADMIN"
        PREMIUM = "PREMIUM"
        STANDARD = "STANDARD"

    account_tier = models.CharField(
        max_length=10,
        choices=AccountTier.choices,
        default=AccountTier.STANDARD
    )

    timezone = models.CharField(max_length=50, default='UTC')
    preferred_currency = models.CharField(max_length=10, default='USD')

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True,blank=True)

    is_staff = models.BooleanField(default=False) 
    
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    def soft_delete(self):
        self.is_active = False
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
