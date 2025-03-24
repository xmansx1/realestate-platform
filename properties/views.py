# views.py - نسخة مصححة

import io
import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.http import urlencode
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from .models import Property, PropertyImage, PropertyRequest
from .forms import PropertyForm, PropertyImageForm, PropertyRequestForm


# الصفحة الرئيسية
def home(request):
    all_properties = Property.objects.all().order_by('-created_at')
    property_type = request.GET.get('type')
    status = request.GET.get('status')
    city = request.GET.get('city')

    if property_type:
        all_properties = all_properties.filter(property_type=property_type)

    if status:
        status_db_value = 'sell' if status == 'sale' else status
        all_properties = all_properties.filter(request_type=status_db_value)
    else:
        status_db_value = None

    if city:
        all_properties = all_properties.filter(city__icontains=city)

    if status_db_value:
        properties_for_sale = all_properties if status_db_value == 'sell' else Property.objects.none()
        properties_for_rent = all_properties if status_db_value == 'rent' else Property.objects.none()
    else:
        properties_for_sale = all_properties.filter(request_type='sell')
        properties_for_rent = all_properties.filter(request_type='rent')

    filters = {'type': property_type, 'status': status, 'city': city}

    return render(request, 'properties/home.html', {
        'properties_for_sale': properties_for_sale,
        'properties_for_rent': properties_for_rent,
        'filters': filters,
    })


def create_property_request(request):
    if request.method == 'POST':
        form = PropertyRequestForm(request.POST)
        if form.is_valid():
            prop_request = form.save(commit=False)
            prop_request.user = request.user if request.user.is_authenticated else User.objects.filter(is_superuser=True).first()
            prop_request.save()
            messages.success(request, "تم إرسال الطلب بنجاح ✅")
            return redirect('create_property_request')
    else:
        form = PropertyRequestForm()
    return render(request, 'properties/request_form.html', {'form': form})


@login_required
def my_requests(request):
    requests = PropertyRequest.objects.filter(user=request.user)
    return render(request, 'properties/my_requests.html', {'requests': requests})


@login_required
def edit_request(request, request_id):
    if not request.user.is_superuser:
        messages.error(request, "غير مصرح لك بالتعديل.")
        return redirect('property_requests')
    
    property_request = get_object_or_404(PropertyRequest, id=request_id)
    if request.method == 'POST':
        form = PropertyRequestForm(request.POST, instance=property_request)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تحديث الطلب بنجاح ✅")
            return redirect('property_requests')
    else:
        form = PropertyRequestForm(instance=property_request)
    return render(request, 'properties/edit_request.html', {'form': form})


@login_required
def delete_request(request, request_id):
    if not request.user.is_superuser:
        messages.error(request, "غير مصرح لك بالحذف.")
        return redirect('property_requests')

    property_request = get_object_or_404(PropertyRequest, id=request_id)
    if request.method == 'POST':
        property_request.delete()
        messages.success(request, "تم حذف الطلب بنجاح ✅")
        return redirect('property_requests')
    return render(request, 'properties/delete_confirm.html', {'request_obj': property_request})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "تم إنشاء الحساب بنجاح!")
            return redirect("home")
        else:
            messages.error(request, "حدث خطأ أثناء إنشاء الحساب.")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def export_requests_excel(request):
    requests = PropertyRequest.objects.filter(user=request.user).values(
        'full_name', 'phone', 'property_type', 'request_type', 'owner_type',
        'city', 'district', 'area', 'details')
    df = pd.DataFrame(list(requests))
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='طلبات المستخدم')
    response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=requests.xlsx'
    return response


@login_required
def property_requests(request):
    requests = PropertyRequest.objects.all()
    return render(request, 'properties/property_requests.html', {'requests': requests})


def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    message = f"""مرحبًا، أنا مهتم بالعقار التالي:\n- نوع العقار: {property.get_property_type_display()}\n- المدينة: {property.city}\n- الحي: {property.district}\n- المساحة: {property.area} م²\n- السعر: {property.price if property.price else 'غير محدد'} ريال\nهل لا يزال متاحًا؟"""
    whatsapp_message = urlencode({'text': message})
    phone = f"966{property.phone[1:]}" if property.phone.startswith("0") else property.phone
    return render(request, "properties/property_detail.html", {
        "property": property,
        "whatsapp_message": whatsapp_message,
        "whatsapp_number": phone,
    })


    
from django.contrib import messages  # تأكد من استيراده

@login_required
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)  # ✅ تم تمرير request.FILES
        files = request.FILES.getlist('images')  # ✅ الحصول على الصور المرفوعة

        if form.is_valid():
            property = form.save(commit=False)
            property.user = request.user
            property.save()

            # ✅ حفظ الصور المرتبطة بالعقار
            for f in files:
                PropertyImage.objects.create(property=property, image=f)

            messages.success(request, "✅ تم إضافة العقار بنجاح.")
            return redirect('dashboard')
        else:
            messages.error(request, "❌ حدث خطأ أثناء حفظ البيانات، تأكد من الحقول.")
    else:
        form = PropertyForm()

    context = {'form': form}
    return render(request, 'properties/add_property.html', context)




@login_required
def my_properties(request):
    properties = Property.objects.filter(user=request.user)
    return render(request, 'properties/my_properties.html', {'properties': properties})


@login_required
def edit_property(request, pk):
    property = get_object_or_404(Property, pk=pk, user=request.user)
    images = property.propertyimage_set.all()
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property)
        new_images = request.FILES.getlist('images')
        if form.is_valid():
            form.save()
            for img in new_images:
                PropertyImage.objects.create(property=property, image=img)
            messages.success(request, "تم تحديث العقار بنجاح ✅")
            return redirect('my_properties')
        else:
            messages.error(request, "حدث خطأ أثناء التحديث ❌")
    else:
        form = PropertyForm(instance=property)
    return render(request, 'properties/edit_property.html', {'form': form, 'property': property, 'images': images})


@login_required
def delete_property(request, pk):
    property = get_object_or_404(Property, pk=pk, user=request.user)
    if request.method == 'POST':
        property.delete()
        return redirect('my_properties')
    return render(request, 'properties/delete_property.html', {'property': property})


@login_required
def dashboard(request):
    total_requests = PropertyRequest.objects.filter(user=request.user).count()
    total_properties = Property.objects.filter(user=request.user).count()
    return render(request, 'properties/dashboard.html', {
        'total_requests': total_requests,
        'total_properties': total_properties,
    })


@login_required
def request_property(request, property_id):
    property_obj = get_object_or_404(Property, pk=property_id)
    if request.method == 'POST':
        form = PropertyRequestForm(request.POST)
        if form.is_valid():
            property_request = form.save(commit=False)
            property_request.user = request.user
            property_request.save()
            messages.success(request, "تم إرسال طلبك على العقار بنجاح ✅")
            return redirect('my_requests')
        else:
            messages.error(request, "❌ حدث خطأ أثناء إرسال الطلب.")
    else:
        initial_data = {
            'property_type': property_obj.property_type,
            'request_type': property_obj.request_type,
            'owner_type': property_obj.owner_type,
            'city': property_obj.city,
            'district': property_obj.district,
            'area': property_obj.area,
        }
        form = PropertyRequestForm(initial=initial_data)
    return render(request, 'properties/request_form.html', {'form': form, 'property': property_obj})


@login_required
def delete_property_image(request, image_id):
    image = get_object_or_404(PropertyImage, id=image_id, property__user=request.user)
    if request.method == 'POST':
        image.image.delete()
        image.delete()
        messages.success(request, "تم حذف الصورة بنجاح ✅")
        return redirect('edit_property', pk=image.property.id)
    else:
        messages.error(request, "يجب استخدام POST للحذف.")
        return redirect('my_properties')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "✅ تم إضافة المستخدم بنجاح.")
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'properties/add_user.html', {'form': form})


@login_required
def request_detail(request, request_id):
    req = get_object_or_404(PropertyRequest, id=request_id)
    return render(request, 'properties/request_detail.html', {'request_obj': req})
