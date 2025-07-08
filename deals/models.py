# deals/models.py
from django.db import models
from requests.models import RealEstateRequest
from accounts.models import CustomUser
from django.conf import settings

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
