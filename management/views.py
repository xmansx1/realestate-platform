from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Property
from .forms import PropertyForm
from django.shortcuts import get_object_or_404
from .forms import PropertyDocumentForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Property
from .forms import PropertyDocumentsForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UnitForm
from .models import Property, Unit
from .forms import UpdateLogForm
from django.db.models import Count, Sum, Q
from django.views.decorators.http import require_POST
from .models import UpdateLog
from .forms import UpdateLogForm
from .forms import ScheduledMaintenanceForm
from .models import Unit, ScheduledMaintenance
from django.contrib.auth.decorators import user_passes_test

@login_required
def my_properties(request):
    properties = Property.objects.filter(owner=request.user)
    return render(request, 'management/my_properties.html', {'properties': properties})

@login_required
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            prop = form.save(commit=False)
            prop.owner = request.user
            prop.save()
            return redirect('management:my_properties')
    else:
        form = PropertyForm()
    return render(request, 'management/add_property.html', {'form': form})

@login_required
def owner_properties_units(request):
    properties = Property.objects.filter(owner=request.user).prefetch_related('units')
    return render(request, 'management/owner_property_units.html', {'properties': properties})

@login_required
def upload_documents(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id, owner=request.user)

    if request.method == 'POST':
        form = PropertyDocumentForm(request.POST, request.FILES, instance=property_obj)
        if form.is_valid():
            form.save()
            return redirect('management:owner_properties_units')
    else:
        form = PropertyDocumentForm(instance=property_obj)

    return render(request, 'management/upload_documents.html', {'form': form, 'property': property_obj})

@login_required
def property_documents_view(request, pk):
    property = get_object_or_404(Property, pk=pk, owner=request.user)
    return render(request, 'management/property_documents.html', {'property': property})

@login_required
def update_property_documents(request, pk):
    property = get_object_or_404(Property, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = PropertyDocumentsForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ تم تحديث المستندات بنجاح.")
            return redirect('management:property_documents', pk=property.pk)
    else:
        form = PropertyDocumentsForm(instance=property)
    return render(request, 'management/update_documents.html', {'form': form, 'property': property})


@login_required
def add_unit_to_property(request, pk):
    property = get_object_or_404(Property, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.property = property
            unit.save()
            messages.success(request, "✅ تم إضافة الوحدة بنجاح.")
            return redirect('management:property_units', pk=property.pk)
    else:
        form = UnitForm()

    return render(request, 'management/add_unit.html', {
        'form': form,
        'property': property
    })
    
@login_required
def edit_unit(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id, property__owner=request.user)
    
    if request.method == 'POST':
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ تم تحديث بيانات الوحدة بنجاح.")
            return redirect('management:property_units', pk=unit.property.pk)
    else:
        form = UnitForm(instance=unit)

    return render(request, 'management/edit_unit.html', {
        'form': form,
        'unit': unit
    })


@login_required
def unit_detail_view(request, pk):
    unit = get_object_or_404(
        Unit.objects.select_related('property', 'rental_info'),
        pk=pk,
        property__owner=request.user
    )
    
    rental_info = getattr(unit, 'rental_info', None)
    updates = unit.updates.all().order_by('-date')
    scheduled_maintenances = unit.scheduledmaintenance_set.all().order_by('-date')

    context = {
        'unit': unit,
        'rental_info': rental_info,
        'updates': updates,
        'scheduled_maintenances': scheduled_maintenances,
    }
    return render(request, 'management/unit_detail.html', context)

@login_required
def edit_unit(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id, property__owner=request.user)

    if request.method == 'POST':
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ تم تحديث بيانات الوحدة بنجاح.")
            return redirect('management:property_units', pk=unit.property.id)
    else:
        form = UnitForm(instance=unit)

    return render(request, 'management/edit_unit.html', {
        'form': form,
        'unit': unit
    })
    
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Unit

@login_required
def unit_detail(request, unit_id):
    unit = get_object_or_404(
        Unit.objects.select_related('property', 'rental_info').prefetch_related('updates', 'scheduled_maintenances'),
        id=unit_id,
        property__owner=request.user
    )

    context = {
        'unit': unit,
        'rental_info': getattr(unit, 'rental_info', None),
        'updates': unit.updates.order_by('-date'),
        'scheduled_maintenances': unit.scheduled_maintenances.order_by('-scheduled_date'),
    }
    return render(request, 'management/unit_detail.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Unit, RentalInfo
from .forms import RentalInfoForm
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def add_rental_info(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)

    # تأكد أنه لا يوجد عقد إيجار مكرر
    if hasattr(unit, 'rental_info'):
        messages.error(request, "هذه الوحدة لديها عقد إيجار مسجل بالفعل.")
        return redirect('management:unit_detail', pk=unit.id)

    if request.method == 'POST':
        form = RentalInfoForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.unit = unit
            rental.save()
            messages.success(request, "تم حفظ عقد الإيجار بنجاح.")
            return redirect('management:unit_detail', pk=unit.id)
    else:
        form = RentalInfoForm(initial={'unit': unit})

    return render(request, 'management/add_rental_info.html', {
        'form': form,
        'unit': unit
    })

@login_required
def unit_updates_view(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id, property__owner=request.user)
    updates = unit.updates.all().order_by('-date')
    return render(request, 'management/unit_updates.html', {
        'unit': unit,
        'updates': updates
    })
    

@login_required
def add_unit_update(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id, property__owner=request.user)

    if request.method == 'POST':
        form = UpdateLogForm(request.POST, request.FILES)
        if form.is_valid():
            update = form.save(commit=False)
            update.unit = unit
            update.save()
            messages.success(request, "✅ تم إضافة التحديث / المصروف بنجاح.")
            return redirect('management:unit_updates', unit_id=unit.id)
    else:
        form = UpdateLogForm()

    return render(request, 'management/add_unit_update.html', {
        'form': form,
        'unit': unit,
    })
    
@staff_member_required
def edit_rental_info(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)
    rental = get_object_or_404(RentalInfo, unit=unit)

    if request.method == 'POST':
        form = RentalInfoForm(request.POST, instance=rental)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تحديث عقد الإيجار بنجاح.")
            return redirect('management:unit_detail', pk=unit.id)
    else:
        form = RentalInfoForm(instance=rental)

    return render(request, 'management/edit_rental_info.html', {
        'form': form,
        'unit': unit
    })
    
@login_required
def delete_unit(request, pk):
    unit = get_object_or_404(Unit, pk=pk, property__owner=request.user)
    property_id = unit.property.id  # للرجوع بعد الحذف
    unit.delete()
    messages.success(request, "✅ تم حذف الوحدة بنجاح.")
    return redirect('management:property_units', pk=property_id)

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from datetime import date
from .models import Unit, UpdateLog

@login_required
def delete_rental_info(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id, property__owner=request.user)
    rental_info = getattr(unit, 'rental_info', None)

    if rental_info:
        tenant_name = rental_info.tenant_name
        rental_info.delete()

        # 📝 سجل عملية الحذف
        UpdateLog.objects.create(
            unit=unit,
            update_type=f"📄 حذف عقد الإيجار ({tenant_name})",
            date=date.today()
        )

        messages.success(request, "✅ تم حذف عقد الإيجار بنجاح.")
    else:
        messages.warning(request, "⚠️ لا يوجد عقد إيجار مرتبط بهذه الوحدة.")

    return redirect('management:unit_detail', pk=unit.id)

@login_required
def edit_unit_update(request, update_id):
    update = get_object_or_404(
        UpdateLog,
        pk=update_id,
        unit__property__owner=request.user  # التأكد من ملكية العقار
    )
    unit = update.unit

    if request.method == 'POST':
        form = UpdateLogForm(request.POST, request.FILES, instance=update)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ تم تحديث التحديث / المصروف بنجاح.")
            return redirect('management:unit_detail', pk=unit.pk)
        else:
            messages.error(request, "حدث خطأ أثناء حفظ البيانات. تأكد من صحة المدخلات.")
    else:
        form = UpdateLogForm(instance=update)

    return render(request, 'management/edit_unit_update.html', {
        'form': form,
        'unit': unit,
        'update': update,
    })
    

@login_required
def delete_unit_update(request, update_id):
    update = get_object_or_404(UpdateLog, pk=update_id, unit__property__owner=request.user)
    unit = update.unit

    if request.method == 'POST':
        update.delete()
        messages.success(request, "🗑️ تم حذف التحديث / المصروف بنجاح.")
        return redirect('management:unit_detail', pk=unit.pk)

    return render(request, 'management/delete_unit_update.html', {
        'update': update,
        'unit': unit,
    })


@login_required
def owner_report(request):
    properties = Property.objects.filter(owner=request.user).prefetch_related('units')

    total_units = Unit.objects.filter(property__in=properties).count()
    rented_units = Unit.objects.filter(property__in=properties, status='rented').count()
    available_units = Unit.objects.filter(property__in=properties, status='available').count()

    total_rent = RentalInfo.objects.filter(unit__property__in=properties).aggregate(total=Sum('amount'))['total'] or 0
    total_updates = UpdateLog.objects.filter(unit__property__in=properties).count()

    context = {
        'properties': properties,
        'total_units': total_units,
        'rented_units': rented_units,
        'available_units': available_units,
        'total_rent': total_rent,
        'total_updates': total_updates,
    }
    return render(request, 'management/owner_report.html', context)

@login_required
def schedule_maintenance(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)
    if request.method == 'POST':
        form = ScheduledMaintenanceForm(request.POST)
        if form.is_valid():
            maintenance = form.save(commit=False)
            maintenance.unit = unit
            maintenance.save()
            messages.success(request, "✅ تم تسجيل الصيانة المجدولة بنجاح.")
            return redirect('management:unit_detail', pk=unit.pk)
    else:
        form = ScheduledMaintenanceForm()
    return render(request, 'management/schedule_maintenance.html', {'form': form, 'unit': unit})


def is_admin(user):
    return user.is_staff  # أو عدلها حسب صلاحيات الموظف الإداري لديك

@login_required
@user_passes_test(is_admin)
def unit_maintenance_list(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    maintenances = ScheduledMaintenance.objects.filter(unit=unit).order_by('-date')

    return render(request, 'management/scheduled_maintenances.html', {
        'unit': unit,
        'maintenances': maintenances,
    })
    
# تأكد من أن المستخدم إداري فقط
def is_admin_staff(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_admin_staff)
def edit_scheduled_maintenance(request, pk):
    maintenance = get_object_or_404(ScheduledMaintenance, pk=pk)

    if request.method == 'POST':
        form = ScheduledMaintenanceForm(request.POST, instance=maintenance)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ تم تعديل الصيانة المجدولة بنجاح.")
            return redirect('management:unit_detail', pk=maintenance.unit.pk)
    else:
        form = ScheduledMaintenanceForm(instance=maintenance)

    return render(request, 'management/edit_maintenance.html', {
        'form': form,
        'maintenance': maintenance
    })
    
@login_required
@user_passes_test(is_admin_staff)
def delete_scheduled_maintenance(request, pk):
    maintenance = get_object_or_404(ScheduledMaintenance, pk=pk)

    if request.method == 'POST':
        unit_id = maintenance.unit.pk
        maintenance.delete()
        messages.success(request, "🗑️ تم حذف الصيانة المجدولة بنجاح.")
        return redirect('management:unit_detail', pk=unit_id)

    return render(request, 'management/confirm_delete_maintenance.html', {
        'maintenance': maintenance
    })



@staff_member_required
def admin_properties_view(request):
    properties = Property.objects.all()
    context = {
        'properties': properties
    }
    return render(request, 'properties/admin/admin_properties.html', context)


from django.contrib.auth import get_user_model

User = get_user_model()

@staff_member_required
def assign_staff(request, unit_id, user_id):
    unit = get_object_or_404(Unit, id=unit_id)
    user = get_object_or_404(User, id=user_id, is_staff=True)
    unit.assigned_to = user
    unit.save()
    return redirect('management:unit_detail', pk=unit.id)
from accounts.models import CustomUser 

@staff_member_required
def assign_staff_view(request):
    units = Unit.objects.filter(assigned_to__isnull=True)
    staff_users = CustomUser.objects.filter(is_staff=True)

    if request.method == "POST":
        unit_id = request.POST.get("unit_id")
        staff_id = request.POST.get("staff_id")
        unit = get_object_or_404(Unit, id=unit_id)
        staff = get_object_or_404(CustomUser, id=staff_id, is_staff=True)
        unit.assigned_to = staff
        unit.save()
        messages.success(request, f"تم تعيين الموظف {staff.get_full_name()} للوحدة {unit.unit_number}.")
        return redirect('management:assign_staff_view')

    context = {
        'units': units,
        'staff_users': staff_users,
    }
    return render(request, 'management/assign_staff.html', context)

import json
from django.http import JsonResponse

@require_POST
def assign_staff_to_unit(request):
    try:
        data = json.loads(request.body)
        unit_id = data.get("unit_id")
        user_id = data.get("user_id")

        if not unit_id or not user_id:
            return JsonResponse({"success": False, "message": "بيانات غير مكتملة"}, status=400)

        unit = Unit.objects.get(id=unit_id)
        user = get_user_model().objects.get(id=user_id, is_staff=True)

        unit.assigned_to = user
        unit.save()

        return JsonResponse({"success": True})
    except Unit.DoesNotExist:
        return JsonResponse({"success": False, "message": "الوحدة غير موجودة"}, status=404)
    except get_user_model().DoesNotExist:
        return JsonResponse({"success": False, "message": "الموظف غير موجود"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)  
    

from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Unit
from django.contrib.auth import get_user_model
User = get_user_model()

@require_POST
@csrf_exempt  # استخدم فقط إذا لم يعمل csrf_token في الجافاسكربت
@login_required
def assign_staff(request):
    data = json.loads(request.body)
    unit_id = data.get('unit_id')
    user_id = data.get('user_id')

    try:
        unit = Unit.objects.get(id=unit_id)
        staff = User.objects.get(id=user_id)
        unit.staff = staff
        unit.save()
        return JsonResponse({'success': True})
    except Unit.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'الوحدة غير موجودة'})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'الموظف غير موجود'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})