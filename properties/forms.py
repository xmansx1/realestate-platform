from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ['owner', 'status', 'is_approved', 'created_at', 'updated_at', 'created_by']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'property_type': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'contact_info': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'license_number': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'area': forms.NumberInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'city': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'district': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'image': forms.FileInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
        }
