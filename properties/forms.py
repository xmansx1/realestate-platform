from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'description', 'price', 'property_type', 'contact_info', 'license_number','area', 'location', 'latitude', 'longitude', 'image']

