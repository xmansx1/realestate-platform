from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Property
from .forms import PropertyForm

@staff_member_required
def property_list(request):
    status = request.GET.get('status')  # جلب الحالة من URL
    properties = Property.objects.all().order_by('-created_at')

    if status in ['active', 'archived']:
        properties = properties.filter(status=status)

    return render(request, 'properties/admin/list.html', {
        'properties': properties,
        'selected_status': status,
    })


@staff_member_required
def property_create(request):
    form = PropertyForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        property = form.save(commit=False)
        property.created_by = request.user
        property.save()
        return redirect('properties:admin_list')
    return render(request, 'properties/admin/form.html', {'form': form})

@staff_member_required
def property_update(request, pk):
    property = get_object_or_404(Property, pk=pk)
    form = PropertyForm(request.POST or None, request.FILES or None, instance=property)
    if form.is_valid():
        form.save()
        return redirect('properties:admin_list')
    return render(request, 'properties/admin/form.html', {'form': form})

@staff_member_required
def property_delete(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        property.delete()
        return redirect('properties:admin_list')
    return render(request, 'properties/admin/delete_confirm.html', {'property': property})


from django.http import Http404

def property_detail(request, pk):
    try:
        property = Property.objects.get(pk=pk, status='active')
    except Property.DoesNotExist:
        raise Http404("العقار غير موجود أو مؤرشف.")

    return render(request, 'properties/detail.html', {'property': property})

def property_list_view(request):
    properties = Property.objects.filter(status='active')
    return render(request, 'properties/list.html', {'properties': properties})
