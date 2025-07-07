from django import forms
from .models import Property
from .models import Unit
from .models import UpdateLog
from .models import ScheduledMaintenance

class PropertyDocumentForm(forms.ModelForm):
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
            'deed_document': 'صك العقار',
            'insurance_document': 'وثيقة التأمين',
            'sketch_document': 'الكروكي',
            'agency_document': 'وكالة شرعية',
            'other_document': 'مستند آخر',
        }

class PropertyDocumentsForm(forms.ModelForm):
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

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['unit_number', 'area', 'price', 'location', 'status']
        labels = {
            'unit_number': 'رقم الوحدة',
            'area': 'المساحة (م²)',
            'price': 'المبلغ',
            'location': 'الموقع داخل العقار',
            'status': 'حالة الوحدة',
        }   
        
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
        
class ScheduledMaintenanceForm(forms.ModelForm):
    class Meta:
        model = ScheduledMaintenance
        fields = ['maintenance_type', 'scheduled_date', 'description']
        labels = {
            'maintenance_type': 'نوع الصيانة',
            'scheduled_date': 'تاريخ الصيانة',
            'description': 'ملاحظات إضافية',
        }
