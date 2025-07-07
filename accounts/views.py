# accounts/views.py
from notifications.models import Notification
from notifications.models import Notification
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from requests.models import RealEstateRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import (
    AdminLoginForm,
    CustomUserCreationForm,
    CustomUserUpdateForm,
)

from .models import CustomUser

# ✅ دالة التحقق من صلاحية الأدمن
def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

# ✅ تسجيل دخول الأدمن
def admin_login_view(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            user = authenticate(request, phone=phone, password=password)
            if user and user.role == 'admin':
                login(request, user)
                return redirect('accounts:admin_dashboard')
            messages.error(request, "بيانات الدخول غير صحيحة أو ليس لديك صلاحية.")
    else:
        form = AdminLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def admin_logout_view(request):
    logout(request)
    messages.success(request, "🚪 تم تسجيل الخروج بنجاح.")
    return redirect('accounts:admin_login')

# ✅ لوحة تحكم الأدمن
@login_required
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    total_requests = RealEstateRequest.objects.count()
    new_requests = RealEstateRequest.objects.filter(status='new').count()
    reviewed_requests = RealEstateRequest.objects.filter(status='reviewed').count()
    contacted_requests = RealEstateRequest.objects.filter(status='contacted').count()

    # ✅ تعريف المتغير المستخدم في القالب
    unread_notifications = Notification.objects.filter(recipient=request.user, is_read=False).count()

    context = {
        'total_requests': total_requests,
        'new_requests': new_requests,
        'reviewed_requests': reviewed_requests,
        'contacted_requests': contacted_requests,
        'unread_notifications': unread_notifications,
    }

    return render(request, 'accounts/admin_dashboard.html', context)

# ✅ عرض المستخدمين
@staff_member_required
def user_list_view(request):
    users = get_user_model().objects.all().order_by('-date_joined')
    return render(request, 'accounts/user_list.html', {'users': users})

# ✅ إنشاء مستخدم جديد
@staff_member_required
def user_create_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "✅ تم إنشاء المستخدم بنجاح.")
            return redirect('accounts:user_list')
        else:
            messages.error(request, "يرجى تصحيح الأخطاء.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/user_create.html', {'form': form})

# ✅ تعديل بيانات المستخدم
@staff_member_required
def user_edit_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ تم تحديث بيانات المستخدم.')
            return redirect('accounts:user_list')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء.')
    else:
        form = CustomUserUpdateForm(instance=user)
    return render(request, 'accounts/user_edit.html', {'form': form, 'user_obj': user})

# ✅ تفعيل / تعطيل المستخدم
@staff_member_required
def toggle_user_status(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = not user.is_active
    user.save()
    status = 'مفعل' if user.is_active else 'موقوف'
    messages.success(request, f"✅ تم تحديث حالة المستخدم إلى: {status}")
    return HttpResponseRedirect(reverse('accounts:user_list'))



@staff_member_required
def user_delete_view(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)

    if request.method == 'POST':
        user.delete()
        messages.success(request, '✅ تم حذف المستخدم بنجاح.')
        return HttpResponseRedirect(reverse('accounts:user_list'))

    messages.error(request, 'حدث خطأ أثناء محاولة الحذف.')
    return HttpResponseRedirect(reverse('accounts:user_list'))

def login_view(request):
    return render(request, 'accounts/login.html')

