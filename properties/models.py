from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

class Property(models.Model):
    STATUS_CHOICES = [
        ('active', 'نشط'),
        ('archived', 'مؤرشف'),
        ('pending', 'قيد المراجعة'),
    ]

    TYPE_CHOICES = [
        ('sale', 'بيع'),
        ('rent', 'إيجار'),
    ]

    title = models.CharField(max_length=255, verbose_name="عنوان العقار")
    description = models.TextField(verbose_name="وصف العقار")

    price = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="السعر"
    )

    property_type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="نوع العرض")
    contact_info = models.CharField(max_length=255, verbose_name="وسيلة التواصل")
    license_number = models.CharField(max_length=100, verbose_name="رقم ترخيص الإعلان", null=True, blank=True)

    area = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="المساحة بالمتر²", null=True, blank=True
    )

    # ✅ الحقول الجديدة
    city = models.CharField(max_length=100, verbose_name="المدينة")
    district = models.CharField(max_length=100, verbose_name="الحي")

    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="خط العرض")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="خط الطول")

    image = models.ImageField(upload_to="properties/", null=True, blank=True, verbose_name="صورة")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active', verbose_name="الحالة", editable=False)
    is_approved = models.BooleanField(default=False, verbose_name="تم الاعتماد من الإدارة")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, verbose_name="تم الإضافة بواسطة")

    def __str__(self):
        return self.title


    @property
    def publisher_name(self):
        return self.created_by.username if self.created_by else "غير محدد"

    class Meta:
        ordering = ['-created_at']
