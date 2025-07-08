from django.shortcuts import render

from properties.models import Property

from properties.models import Property

def home_view(request):
    sale_properties = Property.objects.filter(
        is_approved=True,
        status='active',
        property_type='sale'
    )[:6]

    rent_properties = Property.objects.filter(
        is_approved=True,
        status='active',
        property_type='rent'
    )[:6]

    return render(request, 'home.html', {
        'sale_properties': sale_properties,
        'rent_properties': rent_properties
    })