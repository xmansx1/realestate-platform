from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='المستلم'
    )
    title = models.CharField(max_length=255, verbose_name='عنوان التنبيه')
    message = models.TextField(blank=True, null=True, verbose_name='نص التنبيه')
    is_read = models.BooleanField(default=False, verbose_name='تمت قراءته؟')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'تنبيه'
        verbose_name_plural = 'التنبيهات'

    def __str__(self):
        return self.title
