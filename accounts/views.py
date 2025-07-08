from notifications.models import Notification
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import (
    AdminLoginForm,
    CustomUserCreationForm,
    CustomUserUpdateForm,
)
from deals.models import Deal

from .models import CustomUser
from requests.models import RealEstateRequest
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from requests.models import RealEstateRequest
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy

# ===== Helpers =====

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

# ===== تسجيل الدخول =====

def admin_login_view(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            user = authenticate(request, username=phone, password=password)
            if user and user.role == 'admin':
                login(request, user)
                return redirect('accounts:admin_dashboard')
            messages.error(request, "بيانات الدخول غير صحيحة أو ليس لديك صلاحية.")
    else:
        form = AdminLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def agent_login_view(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)  # يمكنك استبداله بنموذج خاص لو رغبت
        if form.is_valid():
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            user = authenticate(request, username=phone, password=password)
            if user and user.role == 'agent' and user.is_active:
                login(request, user)
                return redirect('requests:agent_available')
            messages.error(request, "بيانات الدخول غير صحيحة أو ليس لديك صلاحية.")
    else:
        form = AdminLoginForm()
    return render(request, 'accounts/agent_login.html', {'form': form})

def unified_login_view(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            user = authenticate(request, username=phone, password=password)
            if user and user.is_active:
                login(request, user)
                if user.role == 'admin':
                    return redirect('accounts:admin_dashboard')
                elif user.role == 'agent':
                    return redirect('requests:agent_dashboard')
                elif user.role == 'owner':
                    return redirect('management:my_properties')
                elif user.role == 'manager':
                    return redirect('management:dashboard')
                else:
                    messages.error(request, "دور المستخدم غير معروف.")
            else:
                messages.error(request, "بيانات الدخول غير صحيحة أو الحساب غير مفعل.")
    else:
        form = AdminLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

# ===== تسجيل الخروج =====
def admin_logout_view(request):
    logout(request)
    messages.success(request, "تم تسجيل الخروج بنجاح.")
    return redirect('home')  # أو غيّرها إلى اسم الصفحة الرئيسية المناسبة

# ===== لوحة تحكم الأدمن =====

# ===== إدارة المستخدمين (للمشرف فقط) =====

@staff_member_required
def user_list_view(request):
    users = get_user_model().objects.all().order_by('-date_joined')
    return render(request, 'accounts/user_list.html', {'users': users})

@staff_member_required
def user_create_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, "✅ تم إنشاء المستخدم بنجاح.")
            return redirect('accounts:user_list')
        else:
            messages.error(request, "يرجى تصحيح الأخطاء.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/user_create.html', {'form': form})

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

from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import AdminLoginForm



from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect

def custom_logout_view(request):
    """
    تسجيل خروج المستخدم وتفريغ الرسائل المخزنة في الجلسة
    ثم إعادة التوجيه إلى الصفحة الرئيسية.
    """
    logout(request)

    # تفريغ الرسائل لمنع ظهورها بعد تسجيل الخروج
    storage = messages.get_messages(request)
    for _ in storage:
        pass

    return redirect('home')  # غيّر 'home' إذا كانت الصفحة الرئيسية باسم مختلف


from django.db.models import Sum, Count
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from requests.models import RealEstateRequest
# تأكد أن كلا النموذجين موجودين هنا


@staff_member_required
def admin_dashboard(request):
    # ✅ عدد جميع الطلبات العقارية
    total_requests = RealEstateRequest.objects.count()

    # ✅ عدد الطلبات المنفذة (من RealEstateRequest مباشرة)
    total_executed = RealEstateRequest.objects.filter(status='executed').count()

    # ✅ إجمالي العمولات لجميع الوسطاء
    total_commission = Deal.objects.aggregate(
        total=Sum('commission')
    )['total'] or 0

    # ✅ إجمالي حصة المنصة
    platform_share = Deal.objects.aggregate(
        total=Sum('platform_share')
    )['total'] or 0

    context = {
        'stats': {
            'total_requests': total_requests,
            'total_executed': total_executed,
            'total_commission': total_commission,
            'platform_share': platform_share,
        },
        'now': timezone.now(),
    }

    return render(request, 'accounts/admin_dashboard.html', context)

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import CustomUser  # تأكد من اسم النموذج المستخدم

@staff_member_required
def manage_users(request):
    users = CustomUser.objects.all().order_by('-date_joined')
    return render(request, 'accounts/manage_users.html', {
        'users': users,
    })
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def owner_dashboard(request):
    return render(request, 'accounts/owner_dashboard.html')