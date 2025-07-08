from django import forms
from .models import (
    Property, Unit, RentalContract, UpdateLog,
    ScheduledMaintenance, PropertyDocument,
    Expense
)


# 🔹 نموذج العقار
class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ['owner', 'is_approved']
        labels = {
            'name': 'اسم العقار',
            'city': 'المدينة',
            'district': 'الحي',
            'latitude': 'خط العرض',
            'longitude': 'خط الطول',
        }

# 🔹 مستندات ضمن نموذج العقار (مباشرة)
class InlinePropertyDocumentForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'deed_document',
            'insurance_document',
            'sketch_document',
            'agency_document',
            'other_document',
        ]
        labels = {
            'deed_document': 'صك الملكية',
            'insurance_document': 'وثيقة التأمين',
            'sketch_document': 'الكروكي',
            'agency_document': 'وكالة شرعية',
            'other_document': 'مستند آخر',
        }

# 🔹 مستندات خارجية مرفوعة يدويًا
class PropertyDocumentForm(forms.ModelForm):
    class Meta:
        model = PropertyDocument
        fields = ['file', 'description']
        widgets = {
            'description': forms.TextInput(attrs={
                'placeholder': 'وصف المستند (اختياري)',
                'class': 'w-full p-2 border rounded-md'
            }),
            'file': forms.ClearableFileInput(attrs={
                'class': 'w-full p-2 border rounded-md'
            }),
        }

# 🔹 نموذج الوحدة
class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        exclude = ['property', 'created_at']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

# 🔹 تحديث بيانات الوحدة (وليس سجل التحديثات)
class UnitUpdateForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['unit_number', 'area', 'price', 'location', 'status', 'notes']

# 🔹 عقد الإيجار
class RentalContractForm(forms.ModelForm):
    class Meta:
        model = RentalContract
        exclude = ['unit', 'created_at']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

# 🔹 التحديثات / المصروفات على الوحدة
class UpdateLogForm(forms.ModelForm):
    class Meta:
        model = UpdateLog
        fields = ['update_type', 'date', 'amount', 'attachment']
        labels = {
            'update_type': 'نوع التحديث / المصروف',
            'date': 'تاريخ التنفيذ',
            'amount': 'المبلغ (اختياري)',
            'attachment': 'مرفق (اختياري)'
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

# 🔹 المصروفات (نموذج مستقل)
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'date', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

# 🔹 صيانة مجدولة
class ScheduledMaintenanceForm(forms.ModelForm):
    class Meta:
        model = ScheduledMaintenance
        fields = ['maintenance_type', 'scheduled_date', 'description']
        labels = {
            'maintenance_type': 'نوع الصيانة',
            'scheduled_date': 'تاريخ الصيانة',
            'description': 'ملاحظات إضافية',
        }
