from django import forms
from .models import RealEstateRequest

class RealEstateRequestForm(forms.ModelForm):
    class Meta:
        model = RealEstateRequest
        fields = [
            'full_name',
            'phone_number',
            'purpose',
            'city',
            'district',
            'property_type',
            'area',
            'budget',
            'message',
        ]

        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input'}),
            'purpose': forms.Select(attrs={'class': 'form-select'}),
            'city': forms.TextInput(attrs={'class': 'form-input'}),
            'district': forms.TextInput(attrs={'class': 'form-input'}),
            'property_type': forms.Select(attrs={'class': 'form-select'}),
            'area': forms.NumberInput(attrs={'class': 'form-input'}),
            'budget': forms.NumberInput(attrs={'class': 'form-input'}),
            'message': forms.Textarea(attrs={'class': 'form-textarea'}),
        }

from django import forms
from .models import RealEstateRequest

class RealEstateRequestStatusForm(forms.ModelForm):
    class Meta:
        model = RealEstateRequest
        fields = ['status']
        labels = {
            'status': 'حالة الطلب',
        }
        widgets = {
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 rounded-md border border-gray-300 focus:outline-none focus:ring focus:ring-green-200'
            })
        }
