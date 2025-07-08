from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.db.models import Sum
from management.models import Unit, RentalContract, UpdateLog, Expense
from properties.models import Property
from properties.forms import PropertyForm
from management.forms import UnitForm, UnitUpdateForm, ExpenseForm, RentalContractForm

@login_required
def owner_dashboard_view(request):
    if request.user.role != 'owner':
        return HttpResponseForbidden("غير مصرح لك بالدخول هنا.")
    return render(request, 'ownership/owner_dashboard.html')


@login_required
def my_properties_view(request):
    if request.user.role != 'owner':
        return HttpResponseForbidden("غير مصرح لك.")
    properties = Property.objects.filter(owner=request.user)
    return render(request, 'ownership/my_properties.html', {'properties': properties})


@login_required
def add_property_view(request):
    if request.user.role != 'owner':
        return HttpResponseForbidden("غير مصرح لك.")
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.owner = request.user
            property.save()
            return redirect('ownership:my_properties')
    else:
        form = PropertyForm()
    return render(request, 'ownership/add_property.html', {'form': form})


@login_required
def edit_property_view(request, pk):
    if request.user.role != 'owner':
        return HttpResponseForbidden("غير مصرح لك.")
    property = get_object_or_404(Property, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            form.save()
            return redirect('ownership:my_properties')
    else:
        form = PropertyForm(instance=property)
    return render(request, 'ownership/edit_property.html', {'form': form, 'property': property})


@login_required
def property_detail_view(request, pk):
    if request.user.role != 'owner':
        return HttpResponseForbidden("غير مصرح لك.")
    property = get_object_or_404(Property, pk=pk, owner=request.user)
    return render(request, 'ownership/property_detail.html', {'property': property})


@login_required
def property_units_view(request, property_id):
    if request.user.role != 'owner':
        return HttpResponseForbidden("غير مصرح لك.")
    property = get_object_or_404(Property, pk=property_id, owner=request.user)
    units = Unit.objects.filter(property=property)
    return render(request, 'ownership/property_units.html', {'property': property, 'units': units})


@login_required
def add_unit_view(request, property_id):
    if request.user.role != 'owner':
        return HttpResponseForbidden("غير مصرح لك.")
    property = get_object_or_404(Property, pk=property_id, owner=request.user)
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.property = property
            unit.save()
            return redirect('ownership:property_units', property_id=property.pk)
    else:
        form = UnitForm()
    return render(request, 'ownership/add_unit.html', {'form': form, 'property': property})


@login_required
def edit_unit_view(request, pk):
    if request.user.role != 'owner':
        return HttpResponseForbidden("غير مصرح لك.")
    unit = get_object_or_404(Unit, pk=pk, property__owner=request.user)
    if request.method == 'POST':
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect('ownership:property_units', property_id=unit.property.pk)
    else:
        form = UnitForm(instance=unit)
    return render(request, 'ownership/edit_unit.html', {'form': form, 'unit': unit})


@login_required
def unit_detail_view(request, pk):
    if request.user.role != 'owner':
        return HttpResponseForbidden("غير مصرح لك.")
    unit = get_object_or_404(Unit.objects.select_related('property'), pk=pk, property__owner=request.user)
    rental_info = getattr(unit, 'rental_contract', None)
    updates = unit.updates.order_by('-date')
    expenses = unit.expenses.order_by('-date')
    context = {
        'unit': unit,
        'rental_info': rental_info,
        'updates': updates,
        'expenses': expenses,
    }
    return render(request, 'ownership/unit_detail.html', context)


@login_required
def add_rental_contract_view(request, pk):
    if request.user.role != 'owner':
        return HttpResponseForbidden("غير مصرح لك.")
    unit = get_object_or_404(Unit, pk=pk, property__owner=request.user)
    if hasattr(unit, 'rental_contract'):
        return HttpResponseForbidden("يوجد عقد إيجار بالفعل لهذه الوحدة.")
    if request.method == 'POST':
        form = RentalContractForm(request.POST)
        if form.is_valid():
            contract = form.save(commit=False)
            contract.unit = unit
            contract.save()
            return redirect('ownership:unit_detail', pk=unit.pk)
    else:
        form = RentalContractForm()
    return render(request, 'ownership/add_rental_contract.html', {'form': form, 'unit': unit})


@login_required
def add_unit_update_view(request, pk):
    if request.user.role != 'owner':
        return HttpResponseForbidden("غير مصرح لك.")
    unit = get_object_or_404(Unit, pk=pk, property__owner=request.user)
    if request.method == 'POST':
        form = UnitUpdateForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.unit = unit
            update.save()
            return redirect('ownership:unit_detail', pk=unit.pk)
    else:
        form = UnitUpdateForm()
    return render(request, 'ownership/add_unit_update.html', {'form': form, 'unit': unit})


@login_required
def add_unit_expense_view(request, pk):
    if request.user.role != 'owner':
        return HttpResponseForbidden("غير مصرح لك.")
    unit = get_object_or_404(Unit, pk=pk, property__owner=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.unit = unit
            expense.save()
            return redirect('ownership:unit_detail', pk=unit.pk)
    else:
        form = ExpenseForm()
    return render(request, 'ownership/add_unit_expense.html', {'form': form, 'unit': unit})


@login_required
def delete_unit_view(request, pk):
    if request.user.role != 'owner':
        return HttpResponseForbidden("غير مصرح لك.")
    unit = get_object_or_404(Unit, pk=pk, property__owner=request.user)
    if request.method == 'POST':
        property_id = unit.property.pk
        unit.delete()
        return redirect('ownership:property_units', property_id=property_id)
    return render(request, 'ownership/confirm_delete_unit.html', {'unit': unit})


@login_required
def delete_property_view(request, pk):
    if request.user.role != 'owner':
        return HttpResponseForbidden("غير مصرح لك.")
    property = get_object_or_404(Property, pk=pk, owner=request.user)
    if request.method == 'POST':
        property.delete()
        return redirect('ownership:my_properties')
    return render(request, 'ownership/confirm_delete_property.html', {'property': property})


@login_required
def owner_report_view(request):
    if request.user.role != 'owner':
        return HttpResponseForbidden("غير مصرح لك.")
    properties = Property.objects.filter(owner=request.user)
    units = Unit.objects.filter(property__owner=request.user)
    rented_units = units.filter(rental_contract__isnull=False)
    total_units = units.count()
    rented_units_count = rented_units.count()
    vacant_units = total_units - rented_units_count
    total_rent = RentalContract.objects.filter(unit__property__owner=request.user).aggregate(total=Sum('amount'))['total'] or 0
    total_expenses = Expense.objects.filter(unit__property__owner=request.user).aggregate(total=Sum('amount'))['total'] or 0
    return render(request, 'ownership/owner_report.html', {
        'total_units': total_units,
        'rented_units': rented_units_count,
        'vacant_units': vacant_units,
        'total_rent': total_rent,
        'total_expenses': total_expenses,
        'properties': properties,
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def owner_dashboard(request):
    return render(request, 'ownership/dashboard.html')
