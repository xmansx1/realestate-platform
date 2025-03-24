from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# اختيارات الحقول العامة
PROPERTY_TYPES = [
    ('apartment', 'شقة'),
    ('villa', 'فيلا'),
    ('floor', 'دور'),
    ('land', 'أرض'),
    ('building', 'عمارة'),
]

REQUEST_TYPES = [
    ('sell', 'بيع'),
    ('rent', 'إيجار'),
]

OWNER_TYPES = [
    ('owner', 'مالك مباشر'),
    ('agent', 'وسيط عقاري'),
]


# نموذج العقار الرئيسي
class Property(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    request_type = models.CharField(max_length=10, choices=REQUEST_TYPES)
    owner_type = models.CharField(max_length=10, choices=OWNER_TYPES)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    area = models.FloatField()
    details = models.TextField(blank=True)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(verbose_name="وصف العقار", blank=True, null=True)
    
    FINANCE_CHOICES = [
        (True, 'نعم'),
        (False, 'لا')
    ]
    is_finance_available = models.BooleanField(choices=FINANCE_CHOICES, default=False)

    def __str__(self):
        return f"{self.full_name} - {self.get_property_type_display()}"


# صور العقارات
class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')


# نموذج طلب العقار
class PropertyRequest(models.Model):
    REQUEST_TYPE_CHOICES = [
        ('buy', 'شراء'),
        ('rent', 'استئجار'),
        ('sell', 'بيع'),
    ]
    OWNER_TYPE_CHOICES = [
        ('owner', 'مالك'),
        ('broker', 'وسيط'),
    ]
    PROPERTY_TYPE_CHOICES = [
        ('apartment', 'شقة'),
        ('villa', 'فيلا'),
        ('building', 'عمارة'),
        ('land', 'أرض'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    request_type = models.CharField(max_length=10, choices=REQUEST_TYPE_CHOICES)
    owner_type = models.CharField(max_length=10, choices=OWNER_TYPE_CHOICES)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_request_type_display()} - {self.get_property_type_display()}"

from django.db import models

class News(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان الخبر")
    is_active = models.BooleanField(default=True, verbose_name="مفعل؟")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")

    def __str__(self):
        return self.title

class FooterSettings(models.Model):
    about = models.TextField("نبذة عنا", blank=True)
    whatsapp = models.CharField("رقم الواتساب", max_length=20, blank=True)
    twitter = models.URLField("رابط تويتر", blank=True)
    phone = models.CharField("رقم الهاتف", max_length=20, blank=True)
    snapchat = models.URLField("رابط سناب شات", blank=True)

    def __str__(self):
        return "إعدادات الفوتر"

    class Meta:
        verbose_name = "إعدادات الفوتر"
        verbose_name_plural = "إعدادات الفوتر"
