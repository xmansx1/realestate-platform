from django import forms
from .models import PropertyRequest
from django.db import models


from django import forms
from .models import PropertyRequest

class PropertyRequestForm(forms.ModelForm):
    class Meta:
        model = PropertyRequest
        exclude = ['user']

        labels = {
            'full_name': 'الاسم الكامل',
            'phone': 'رقم الهاتف',
            'property_type': 'نوع العقار',
            'request_type': 'نوع الطلب',
            'owner_type': 'نوع المالك',
            'city': 'المدينة',
            'district': 'الحي',
            'area': 'المساحة',
            'details': 'تفاصيل إضافية',
        }



from django import forms
from .models import Property

from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'property_type',        # نوع العقار
            'request_type',         # نوع الطلب
            'owner_type',           # نوع المالك
            'city',                 # المدينة
            'district',             # الحي
            'area',                 # المساحة
            'price',                # السعر
            'description',          # وصف العقار
            'full_name',            # اسم المالك أو الوسيط
            'phone',                # رقم الهاتف
            'is_finance_available'  # هل يوجد تمويل؟
        ]


        labels = {
            'property_type': 'نوع العقار',
            'request_type': 'نوع الطلب',
            'owner_type': 'نوع المالك',
            'city': 'المدينة',
            'district': 'الحي',
            'area': 'المساحة (م²)',
            'price': 'السعر',
            'description': 'وصف العقار',
            'full_name': 'اسم المالك أو الوسيط',
            'phone': 'رقم الهاتف',
            'is_finance_available': 'هل يوجد تمويل؟',
        }

        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'area': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'is_finance_available': forms.Select(attrs={'class': 'form-select'}),
        }



from django import forms
from django.contrib.auth.models import User

class CreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

 


 
from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'property_type',
            'request_type',
            'owner_type',
            'city',
            'district',
            'area',
            'price',
            'description',
            'full_name',
            'phone',
            'is_finance_available',
 
        ]
    widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),  # ✅ بدون readonly
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'is_finance_available': forms.Select(attrs={'class': 'form-select'}),
        }
from django import forms
from .models import PropertyImage

class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image']

