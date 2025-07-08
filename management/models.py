from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

# -----------------------
# 🔹 Property
# -----------------------
class Property(models.Model):
    name = models.CharField("اسم العقار", max_length=255)
    city = models.CharField("المدينة", max_length=100)
    district = models.CharField("الحي", max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_properties",
        verbose_name="المالك"
    )
    is_approved = models.BooleanField("تمت الموافقة", default=False)

    deed_document = models.FileField("صك الملكية", upload_to='documents/deeds/', blank=True, null=True)
    insurance_document = models.FileField("وثيقة التأمين", upload_to='documents/insurance/', blank=True, null=True)
    sketch_document = models.FileField("الكروكي", upload_to='documents/sketches/', blank=True, null=True)
    agency_document = models.FileField("وكالة شرعية", upload_to='documents/agency/', blank=True, null=True)
    other_document = models.FileField("مستند آخر", upload_to='documents/other/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "عقار"
        verbose_name_plural = "العقارات"


# -----------------------
# 🔹 Unit
# -----------------------
class Unit(models.Model):
    UNIT_STATUS_CHOICES = [
        ('available', 'متاح'),
        ('sold', 'مباع'),
        ('rented', 'مؤجر'),
        ('maintenance', 'صيانة'),
    ]
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='units', verbose_name="العقار")
    unit_number = models.CharField("رقم الوحدة", max_length=50)
    area = models.DecimalField("المساحة (م²)", max_digits=10, decimal_places=2)
    price = models.DecimalField("السعر", max_digits=12, decimal_places=2)
    location = models.CharField("الموقع (اختياري)", max_length=255, blank=True, null=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_units', verbose_name="الموظف المسؤول")
    status = models.CharField("حالة الوحدة", max_length=20, choices=UNIT_STATUS_CHOICES, default='available')
    notes = models.TextField("ملاحظات", blank=True, null=True)
    created_at = models.DateTimeField("تاريخ الإضافة", auto_now_add=True)

    def __str__(self):
        return f"وحدة {self.unit_number} - {self.property.name}"

    class Meta:
        verbose_name = "وحدة"
        verbose_name_plural = "الوحدات"


# -----------------------
# 🔹 RentalContract (عقد الإيجار الموحد)
# -----------------------
class RentalContract(models.Model):
    unit = models.OneToOneField(Unit, on_delete=models.CASCADE, related_name='rental_contract')
    tenant_name = models.CharField(max_length=255, verbose_name="اسم المستأجر")
    tenant_id_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="رقم الهوية")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="رقم الجوال")
    start_date = models.DateField(verbose_name="تاريخ بدء العقد")
    end_date = models.DateField(verbose_name="تاريخ انتهاء العقد")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قيمة الإيجار")
    payment_method = models.CharField(
        max_length=20,
        choices=[('monthly', 'شهري'), ('quarterly', 'ربع سنوي'), ('yearly', 'سنوي')],
        default='monthly',
        verbose_name="طريقة الدفع"
    )
    notes = models.TextField(blank=True, null=True, verbose_name="ملاحظات إضافية")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"عقد إيجار - {self.unit} - {self.tenant_name}"

    class Meta:
        verbose_name = "عقد إيجار"
        verbose_name_plural = "عقود الإيجار"


# -----------------------
# 🔹 UpdateLog (تحديثات / مصروفات عامة)
# -----------------------
class UpdateLog(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='updates', verbose_name="الوحدة")
    update_type = models.CharField("نوع التحديث", max_length=100)
    date = models.DateField("تاريخ التحديث")
    amount = models.DecimalField("المبلغ", max_digits=10, decimal_places=2, blank=True, null=True)
    attachment = models.FileField("مرفق", upload_to='unit_updates/', blank=True, null=True)

    def __str__(self):
        return f"{self.update_type} - {self.unit}"

    class Meta:
        verbose_name = "تحديث/مصروف"
        verbose_name_plural = "التحديثات والمصروفات"


# -----------------------
# 🔹 ScheduledMaintenance
# -----------------------
class ScheduledMaintenance(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, verbose_name="الوحدة", related_name="scheduled_maintenances")
    maintenance_type = models.CharField("نوع الصيانة", max_length=100)
    scheduled_date = models.DateField("تاريخ الصيانة المجدولة")
    description = models.TextField("الوصف", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.maintenance_type} - {self.scheduled_date}"

    class Meta:
        verbose_name = "صيانة مجدولة"
        verbose_name_plural = "الصيانات المجدولة"


# -----------------------
# 🔹 PropertyDocument
# -----------------------
class PropertyDocument(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='property_documents/')
    description = models.CharField(max_length=255, blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"مستند لـ {self.property.name}"

    class Meta:
        verbose_name = "مستند عقار"
        verbose_name_plural = "مستندات العقار"
        ordering = ['-uploaded_at']


# -----------------------
# 🔹 Expense (مصروف مباشر)
# -----------------------
class Expense(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.amount} ريال"

    class Meta:
        verbose_name = "مصروف"
        verbose_name_plural = "المصروفات"
        ordering = ['-date']
