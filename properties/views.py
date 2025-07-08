from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Property
from .forms import PropertyForm


# 👁️ عرض العقارات للزوار والمشرف
def property_detail(request, pk):
    try:
        if request.user.is_staff:
            prop = Property.objects.get(pk=pk)
            template = 'properties/detail.html'

        else:
            prop = Property.objects.get(pk=pk, status='active', is_approved=True)
            template = 'properties/detail_public.html'
    except Property.DoesNotExist:
        raise Http404("العقار غير موجود أو غير مفعل.")
    
    return render(request, template, {'property': prop})


# 🌐 عرض قائمة العقارات النشطة للزوار
def property_list_view(request):
    properties = Property.objects.filter(status='active').order_by('-created_at')
    return render(request, 'properties/list.html', {'properties': properties})


# 🧑‍💼 قائمة العقارات للمشرف
@staff_member_required
def admin_property_list(request):
    status = request.GET.get('status')
    properties = Property.objects.select_related('created_by').all()

    if status == 'active':
        properties = properties.filter(status='active')
    elif status == 'archived':
        properties = properties.filter(status='archived')
    elif status == 'pending':
        properties = properties.exclude(status__in=['active', 'archived'])

    return render(request, 'properties/admin/list.html', {
        'properties': properties.order_by('-id'),
        'selected_status': status or '',
    })


# ✅ اعتماد العقار
@staff_member_required
def admin_approve_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    property_obj.is_approved = True
    property_obj.status = "active"  # ✅ تأكد من وجود هذا السطر
    property_obj.save()
    messages.success(request, "تم اعتماد العقار بنجاح.")
    return redirect('properties:admin_property_list')



# ➕ إنشاء عقار جديد
@staff_member_required
def admin_create_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            prop = form.save(commit=False)
            prop.created_by = request.user
            prop.save()
            messages.success(request, "✅ تم إضافة العقار بنجاح.")
            return redirect('properties:admin_property_list')
    else:
        form = PropertyForm()

    return render(request, 'properties/admin/create.html', {'form': form})


# ✏️ تعديل عقار
@staff_member_required
def admin_edit_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ تم تحديث بيانات العقار.")
            return redirect('properties:admin_list')
    else:
        form = PropertyForm(instance=property_obj)

    return render(request, 'properties/admin/form.html', {
        'form': form,
        'property': property_obj,  # ✅ مهم إذا كان يستخدم في القالب
        'is_edit': True  # يمكن استخدامه لتخصيص العنوان داخل القالب
    })



@staff_member_required
def admin_unapprove_property(request, pk):
    property = get_object_or_404(Property, pk=pk)
    property.is_approved = False
    property.status = 'pending'  # ❌ هذه غير معرفة في STATUS_CHOICES
    property.save()
    messages.warning(request, "تم إلغاء اعتماد العقار.")
    return redirect('properties:admin_property_list')



# 🗑️ حذف عقار
@staff_member_required
def admin_delete_property(request, pk):
    prop = get_object_or_404(Property, pk=pk)

    if request.method == 'POST':
        prop.delete()
        messages.success(request, "🗑️ تم حذف العقار بنجاح.")
        return redirect('properties:admin_property_list')

    return render(request, 'properties/admin/delete_confirm.html', {'property': prop})

@staff_member_required
def admin_list(request):
    properties = Property.objects.all().order_by('-created_at')
    return render(request, 'properties/admin_list.html', {
        'properties': properties
    })