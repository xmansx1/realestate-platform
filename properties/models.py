from django.db import models
from django.contrib.auth import get_user_model

class Property(models.Model):
    STATUS_CHOICES = [
        ('active', 'نشط'),
        ('archived', 'مؤرشف'),
    ]

    TYPE_CHOICES = [
        ('sale', 'بيع'),
        ('rent', 'إيجار'),
    ]

    title = models.CharField(max_length=255, verbose_name="عنوان العقار")
    description = models.TextField(verbose_name="وصف العقار")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="السعر")
    property_type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="نوع العرض")  # ✅ جديد
    contact_info = models.CharField(max_length=255, verbose_name="وسيلة التواصل")  # ✅ جديد
    license_number = models.CharField(max_length=100, verbose_name="رقم ترخيص الإعلان", null=True, blank=True)  # ✅ جديد
    area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="المساحة بالمتر²", null=True, blank=True)

    location = models.CharField(max_length=255, verbose_name="الوصف النصي للموقع")  # يمكن جعله اختيارياً لاحقاً
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="خط العرض")  # ✅ جديد
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="خط الطول")  # ✅ جديد

    image = models.ImageField(upload_to="properties/", null=True, blank=True, verbose_name="صورة")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active', verbose_name="الحالة", editable=False)  # ✅ الآن لا يظهر في النموذج

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, verbose_name="تم الإضافة بواسطة")

    def __str__(self):
        return self.title
