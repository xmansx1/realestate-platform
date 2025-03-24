# باقي الاستيرادات كما هي في الأعلى
import io
from django.forms import modelformset_factory
from .models import Property, PropertyImage
from .forms import PropertyForm, PropertyImageForm
from django.db import models
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Property, PropertyImage, PropertyRequest
from .forms import PropertyForm, PropertyRequestForm
import pandas as pd
from django.contrib.auth.models import User
from django.utils.http import urlencode
from django.contrib.auth.decorators import user_passes_test
from django.forms import modelformset_factory
from .models import Property, PropertyImage
from .forms import PropertyImageForm

# الصفحة الرئيسية
def home(request):
    all_properties = Property.objects.all().order_by('-created_at')

    property_type = request.GET.get('type')
    status = request.GET.get('status')  # "sale" أو "rent"
    city = request.GET.get('city')

    # فلترة حسب نوع العقار
    if property_type:
        all_properties = all_properties.filter(property_type=property_type)

    # تحويل "sale" إلى القيمة الفعلية في قاعدة البيانات وهي "sell"
    if status:
        if status == 'sale':
            status_db_value = 'sell'
        else:
            status_db_value = status
        all_properties = all_properties.filter(request_type=status_db_value)
    else:
        status_db_value = None

    # فلترة حسب المدينة
    if city:
        all_properties = all_properties.filter(city__icontains=city)

    # تقسيم النتائج
    if status_db_value:
        properties_for_sale = all_properties if status_db_value == 'sell' else Property.objects.none()
        properties_for_rent = all_properties if status_db_value == 'rent' else Property.objects.none()
    else:
        properties_for_sale = all_properties.filter(request_type='sell')
        properties_for_rent = all_properties.filter(request_type='rent')

    filters = {
        'type': property_type,
        'status': status,
        'city': city,
    }

    return render(request, 'properties/home.html', {
        'properties_for_sale': properties_for_sale,
        'properties_for_rent': properties_for_rent,
        'filters': filters,
    })


# نموذج طلب عقار - مع تعديل ربط الزوار بالأدمن
def create_property_request(request):
    if request.method == 'POST':
        form = PropertyRequestForm(request.POST)
        if form.is_valid():
            prop_request = form.save(commit=False)

            if request.user.is_authenticated:
                prop_request.user = request.user
            else:
                admin_user = User.objects.filter(is_superuser=True).first()
                prop_request.user = admin_user

            prop_request.save()
            messages.success(request, "تم إرسال الطلب بنجاح ✅")
            return redirect('create_property_request')
    else:
        form = PropertyRequestForm()

    return render(request, 'properties/request_form.html', {'form': form})


# عرض الطلبات الخاصة بالمستخدم
@login_required
def my_requests(request):
    requests = PropertyRequest.objects.filter(user=request.user)
    return render(request, 'properties/my_requests.html', {
        'requests': requests
    })


# تعديل طلب
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


# حذف طلب
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


# إنشاء حساب جديد
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


# تصدير الطلبات إلى Excel
@login_required
def export_requests_excel(request):
    requests = PropertyRequest.objects.filter(user=request.user).values(
        'full_name', 'phone', 'property_type', 'request_type', 'owner_type',
        'city', 'district', 'area', 'details'
    )
    df = pd.DataFrame(list(requests))
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='طلبات المستخدم')
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=requests.xlsx'
    return response


# عرض جميع الطلبات
@login_required
def property_requests(request):
    requests = PropertyRequest.objects.all()
    return render(request, 'properties/property_requests.html', {'requests': requests})


# تفاصيل العقار
def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)

    message = f"""مرحبًا، أنا مهتم بالعقار التالي:
- نوع العقار: {property.get_property_type_display()}
- المدينة: {property.city}
- الحي: {property.district}
- المساحة: {property.area} م²
- السعر: {property.price if property.price else "غير محدد"} ريال
هل لا يزال متاحًا؟"""

    whatsapp_message = urlencode({'text': message})
    local_phone = property.phone
    international_phone = f"966{local_phone[1:]}" if local_phone.startswith("0") else local_phone

    return render(request, "properties/property_detail.html", {
        "property": property,
        "whatsapp_message": whatsapp_message,
        "whatsapp_number": international_phone,
    })


# إضافة عقار
@login_required
@login_required


def add_property(request):
    ImageFormSet = modelformset_factory(PropertyImage, form=PropertyImageForm, extra=0)

    if request.method == 'POST':
        form = PropertyForm(request.POST)
        files = request.FILES.getlist('images')  # ← نحصل على كل الصور

        if form.is_valid():
            property = form.save(commit=False)
            property.user = request.user  # إذا كان العقار مرتبط بمستخدم
            property.save()

            # حفظ كل صورة وربطها بالعقار
            for f in files:
                PropertyImage.objects.create(property=property, image=f)

            return redirect('dashboard')  # أو أي صفحة نجاح
    else:
        form = PropertyForm()

    return render(request, 'add_property.html', {
        'form': form,
    })


# عرض عقارات المستخدم
 
@login_required
def my_properties(request):
    properties = Property.objects.filter(user=request.user)
    return render(request, 'properties/my_properties.html', {'properties': properties})



# تعديل العقار
@login_required
def edit_property(request, pk):
    property = get_object_or_404(Property, pk=pk, user=request.user)
    images = property.propertyimage_set.all()

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property)
        new_images = request.FILES.getlist('images')

        if form.is_valid():
            form.save()

            # ✅ إضافة صور جديدة
            for img in new_images:
                PropertyImage.objects.create(property=property, image=img)

            messages.success(request, "تم تحديث العقار بنجاح ✅")
            return redirect('my_properties')
        else:
            messages.error(request, "حدث خطأ أثناء التحديث ❌")
    else:
        form = PropertyForm(instance=property)

    return render(request, 'properties/edit_property.html', {
        'form': form,
        'property': property,
        'images': images
    })




# حذف عقار
@login_required
def delete_property(request, pk):
    property = get_object_or_404(Property, pk=pk, user=request.user)
    if request.method == 'POST':
        property.delete()
        return redirect('my_properties')
    return render(request, 'properties/delete_property.html', {'property': property})


# لوحة التحكم
@login_required
def dashboard(request):
    total_requests = PropertyRequest.objects.filter(user=request.user).count()
    total_properties = Property.objects.filter(user=request.user).count()
    return render(request, 'properties/dashboard.html', {
        'total_requests': total_requests,
        'total_properties': total_properties,
    })


# تقديم طلب على عقار معين
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

    return render(request, 'properties/request_form.html', {
        'form': form,
        'property': property_obj
    })


# حذف صورة عقار
 
@login_required
def delete_property_image(request, image_id):
    image = get_object_or_404(PropertyImage, id=image_id, property__user=request.user)

    if request.method == 'POST':
        image.image.delete()  # حذف الصورة من MEDIA
        image.delete()        # حذف السجل من قاعدة البيانات
        messages.success(request, "تم حذف الصورة بنجاح ✅")
        return redirect('edit_property', pk=image.property.id)
    else:
        messages.error(request, "يجب استخدام POST للحذف.")
        return redirect('my_properties')


# إضافة مستخدم من قبل المشرف
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


# تفاصيل طلب
@login_required
def request_detail(request, request_id):
    req = get_object_or_404(PropertyRequest, id=request_id)
    return render(request, 'properties/request_detail.html', {'request_obj': req})
