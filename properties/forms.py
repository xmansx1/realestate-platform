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

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ['user', 'created_at']
        widgets = {
            'request_type': forms.Select(attrs={'class': 'form-control'}),
            'owner_type': forms.Select(attrs={'class': 'form-control'}),
            'property_type': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'area': forms.NumberInput(attrs={'class': 'form-control'}),
            'details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
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
            'request_type', 'owner_type', 'property_type',
            'area', 'city', 'district', 'full_name', 'phone',
            'details', 'price', 'is_finance_available'
        ]

