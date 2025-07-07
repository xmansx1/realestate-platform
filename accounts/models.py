# accounts/models.py

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("رقم الجوال مطلوب")
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('المشرف يجب أن يكون is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('المشرف يجب أن يكون is_superuser=True.')

        return self.create_user(phone, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'مدير'),
        ('agent', 'وسيط'),
        ('owner', 'مالك'),
        ('manager', 'موظف إداري'),
    ]

    full_name = models.CharField("الاسم الكامل", max_length=150)
    phone = models.CharField("رقم الجوال", max_length=15, unique=True)
    email = models.EmailField("البريد الإلكتروني", unique=True)
    city = models.CharField("المدينة", max_length=100)
    district = models.CharField("الحي", max_length=100)
    val_license = models.CharField("رقم الرخصة", max_length=50, blank=True, null=True)
    role = models.CharField("الدور", max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField("نشط", default=True)
    is_staff = models.BooleanField("موظف إداري", default=False)
    date_joined = models.DateTimeField("تاريخ الانضمام", auto_now_add=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['full_name', 'email']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.full_name} ({self.phone})"
