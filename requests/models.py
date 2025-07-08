from django.db import models
from django.conf import settings
from django.db import models
from django.conf import settings

class RealEstateRequest(models.Model):
    # حالة الطلب (إدارية)
    STATUS_CHOICES = [
        ('new', 'جديد'),
        ('reviewed', 'تم المراجعة'),
        ('contacted', 'تم التواصل'),
        ('executed', 'تم التنفيذ'),
    ]

    # نوع الطلب من الزائر
    PURPOSE_CHOICES = [
        ('sell', 'بيع'),
        ('buy', 'شراء'),
        ('rent_out', 'تأجير'),
        ('rent', 'استئجار'),
    ]

    # نوع العقار المطلوب
    PROPERTY_TYPE_CHOICES = [
        ('apartment', 'شقة'),
        ('villa', 'فيلا'),
        ('land', 'أرض'),
        ('building', 'عمارة'),
        ('rest_house', 'استراحة'),
        ('other', 'أخرى'),
    ]

    # بيانات الزائر
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    message = models.TextField(blank=True, null=True)

    # بيانات الطلب العقاري
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, verbose_name="نوع الطلب")
    city = models.CharField(max_length=100, verbose_name="المدينة")
    district = models.CharField(max_length=100, verbose_name="الحي")
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES, verbose_name="نوع العقار")
    area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="المساحة بالمتر", blank=True, null=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="السعر المتوقع", blank=True, null=True)

    # حالة الطلب
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False, verbose_name="تمت الموافقة؟")

    # الحجز من الوسيط
    reserved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'agent'},
        related_name='reserved_requests',
        verbose_name='الوسيط الحاجز'
    )
    reserved_at = models.DateTimeField(null=True, blank=True, verbose_name='تاريخ الحجز')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"طلب {self.full_name} - {self.get_purpose_display()} في {self.city}"

    @property
    def is_reserved(self):
        return self.reserved_by is not None

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"طلب {self.full_name} - {self.get_purpose_display()} في {self.city}"

    @property
    def is_reserved(self):
        return self.reserved_by is not None


