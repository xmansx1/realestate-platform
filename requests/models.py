from django.db import models
from django.conf import settings

from django.db import models
from django.conf import settings

class RealEstateRequest(models.Model):
    STATUS_CHOICES = [
        ('new', 'جديد'),
        ('reviewed', 'تم المراجعة'),
        ('contacted', 'تم التواصل'),
    ]

    PURPOSE_CHOICES = [
        ('sell', 'بيع'),
        ('buy', 'شراء'),
        ('rent_out', 'تأجير'),
        ('rent', 'استئجار'),
    ]

    PROPERTY_TYPE_CHOICES = [
        ('apartment', 'شقة'),
        ('villa', 'فيلا'),
        ('land', 'أرض'),
        ('building', 'عمارة'),
        ('rest_house', 'استراحة'),
        ('other', 'أخرى'),
    ]

    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    message = models.TextField(blank=True, null=True)

    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, verbose_name="نوع الطلب")
    city = models.CharField(max_length=100, verbose_name="المدينة")
    district = models.CharField(max_length=100, verbose_name="الحي")
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES, verbose_name="نوع العقار")
    area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="المساحة بالمتر", blank=True, null=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="السعر المتوقع", blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    # ➕ الوسيط الذي حجز الطلب
    reserved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'agent'},
        related_name='reserved_requests',
        verbose_name='الوسيط الحاجز'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"طلب من {self.full_name}"

    @property
    def is_reserved(self):
        return self.reserved_by is not None

class Deal(models.Model):
    request = models.OneToOneField(RealEstateRequest, on_delete=models.CASCADE)
    executed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='deals_executed')
    publisher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='deals_published', blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    commission = models.DecimalField(max_digits=12, decimal_places=2)
    platform_share = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"صفقة #{self.pk} – الطلب {self.request.id}"
