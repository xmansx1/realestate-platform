# requests/views.py
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import RealEstateRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import RealEstateRequest
from django.shortcuts import render, get_object_or_404, redirect
from .models import RealEstateRequest
from .forms import RealEstateRequestForm
from properties.models import Property
from notifications.models import Notification
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from requests.models import RealEstateRequest
from requests.forms import RealEstateRequestStatusForm
from notifications.models import Notification
from django.shortcuts import render
from .models import RealEstateRequest
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, get_object_or_404
from .models import RealEstateRequest
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Deal
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import RealEstateRequest
from django.db import models

def admin_request_list(request):
    status_filter = request.GET.get('status')

    if status_filter:
        requests_qs = RealEstateRequest.objects.filter(status=status_filter)
    else:
        requests_qs = RealEstateRequest.objects.all()

    # ترتيب حسب الأحدث
    requests_qs = requests_qs.order_by('-created_at')

    return render(request, 'requests/admin/list.html', {'requests': requests_qs})


@staff_member_required
def admin_request_detail(request, pk):
    real_request = get_object_or_404(RealEstateRequest, pk=pk)

    old_status = real_request.status  # الاحتفاظ بالحالة السابقة

    if request.method == 'POST':
        form = RealEstateRequestStatusForm(request.POST, instance=real_request)
        if form.is_valid():
            form.save()

            # إذا تم تغيير الحالة إلى "تمت المراجعة"، أضف تنبيهًا
            if old_status == 'new' and real_request.status == 'reviewed':
                Notification.objects.create(
                    recipient=request.user,
                    title="📌 تمت مراجعة طلب عقاري",
                    message=f"تمت مراجعة الطلب رقم #{real_request.id} ({real_request.full_name}) بنجاح."
                )

            return redirect('requests:admin_list')
    else:
        form = RealEstateRequestStatusForm(instance=real_request)

    return render(request, 'requests/admin/detail.html', {
        'request_obj': real_request,
        'form': form,
    })

@staff_member_required
def admin_request_update_status(request, pk):
    real_request = get_object_or_404(RealEstateRequest, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(RealEstateRequest.STATUS_CHOICES):
            real_request.status = new_status
            real_request.save()
        return redirect('requests:admin_list')
    return redirect('requests:admin_detail', pk=pk)




@login_required
def request_list_for_broker(request):
    user = request.user
    if not user.groups.filter(name="وسطاء").exists():
        return render(request, "errors/403.html", status=403)

    requests = RealEstateRequest.objects.filter(
        models.Q(is_reserved=False) | models.Q(reserved_by=user)
    ).order_by('-created_at')

    return render(request, "requests/request_list.html", {
        "requests": requests,
    })

@staff_member_required
def request_detail(request, pk):
    request_obj = get_object_or_404(RealEstateRequest, pk=pk)
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in ["new", "reviewed", "contacted"]:
            request_obj.status = new_status
            request_obj.save()
        return redirect("requests:admin_detail", pk=pk)

    return render(request, "requests/detail.html", {
        "request_obj": request_obj
    })



def create_request(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id)

    if request.method == 'POST':
        form = RealEstateRequestForm(request.POST)
        if form.is_valid():
            real_request = form.save(commit=False)
            real_request.property = property_obj
            real_request.save()
            return redirect('properties:detail', property_id)
    else:
        form = RealEstateRequestForm()

    return render(request, 'requests/create.html', {
        'form': form,
        'property': property_obj,
    })


def create_general_request(request):
    if request.method == 'POST':
        form = RealEstateRequestForm(request.POST)
        if form.is_valid():
            real_request = form.save()

            # إرسال تنبيه للمشرفين
            User = get_user_model()
            admins = User.objects.filter(is_superuser=True)
            for admin in admins:
                Notification.objects.create(
                    recipient=admin,
                    title="📩 طلب عقاري جديد",
                    message=f"تم إرسال طلب جديد من الزائر ({real_request.full_name}) برقم: {real_request.phone_number}",
                )

            # رسالة تأكيد للمستخدم
            messages.success(request, "✅ تم إرسال الطلب بنجاح، سنقوم بالتواصل معك قريبًا.")
            return redirect('home')
    else:
        form = RealEstateRequestForm()
    
    return render(request, 'requests/general_request.html', {'form': form})



@require_POST
@login_required
@user_passes_test(lambda u: u.is_superuser)
def mark_request_as_reviewed(request, pk):
    req = get_object_or_404(RealEstateRequest, pk=pk)
    if req.status == 'new':
        req.status = 'reviewed'
        req.save()
    return redirect('requests:admin_detail', pk=pk)
@require_POST
@login_required
@user_passes_test(lambda u: u.is_superuser)
def mark_request_as_contacted(request, pk):
    req = get_object_or_404(RealEstateRequest, pk=pk)
    if req.status == 'reviewed':
        req.status = 'contacted'
        req.save()

        # إرسال تنبيه للمشرفين الآخرين (غير الذي نفذ العملية)
        User = get_user_model()
        other_admins = User.objects.filter(is_superuser=True).exclude(id=request.user.id)
        for admin in other_admins:
            Notification.objects.create(
                recipient=admin,
                title="📞 تم التواصل مع طلب عقاري",
                message=f"قام {request.user.full_name} بتحديث الطلب من {req.full_name} إلى (تم التواصل).",
            )

    return redirect('requests:admin_detail', pk=pk)



@staff_member_required
def mark_reviewed(request, pk):
    real_request = get_object_or_404(RealEstateRequest, pk=pk)
    if request.method == 'POST':
        real_request.status = 'reviewed'
        real_request.save()
    return redirect('requests:admin_detail', pk=pk)

@staff_member_required
def mark_contacted(request, pk):
    real_request = get_object_or_404(RealEstateRequest, pk=pk)
    if request.method == 'POST':
        real_request.status = 'contacted'
        real_request.save()
    return redirect('requests:admin_detail', pk=pk)

@staff_member_required
@require_POST
def admin_request_delete(request, pk):
    request_obj = get_object_or_404(RealEstateRequest, pk=pk)
    request_obj.delete()
    messages.success(request, "تم حذف الطلب بنجاح.")
    return redirect('requests:admin_list')

def is_agent(user):
    return user.is_authenticated and user.role == 'agent'

@login_required
@user_passes_test(is_agent)
def available_requests_for_agent(request):
    requests = RealEstateRequest.objects.filter(
        status='reviewed',
        reserved_by__isnull=True
    )
    return render(request, 'requests/agent/available_requests.html', {
        'requests': requests
    })

# views.py

@login_required
@user_passes_test(is_agent)
def reserve_request(request, pk):
    real_request = get_object_or_404(RealEstateRequest, pk=pk, reserved_by__isnull=True)

    if request.method == 'POST':
        real_request.reserved_by = request.user
        real_request.save()
        messages.success(request, "✅ تم حجز الطلب بنجاح.")
        return redirect('requests:agent_available')

    return render(request, 'requests/agent/confirm_reserve.html', {
        'request_obj': real_request
    })

@login_required
@user_passes_test(lambda u: u.role == 'agent')
def my_reserved_requests(request):
    requests = RealEstateRequest.objects.filter(reserved_by=request.user)
    return render(request, 'requests/agent/my_requests.html', {'requests': requests})
@login_required
@user_passes_test(lambda u: u.role == 'agent')
def execute_request(request, pk):
    real_request = get_object_or_404(RealEstateRequest, pk=pk, reserved_by=request.user)
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        try:
            amount = float(amount)
        except ValueError:
            messages.error(request, "المبلغ غير صالح.")
            return redirect('requests:agent_my_requests')

        # حساب العمولة
        commission = amount * 0.025
        executed_by_share = commission * 0.8
        publisher_share = 0.0
        platform_share = commission * 0.2

        # في حال كان هناك ناشر مختلف
        if real_request.reserved_by != real_request.created_by and real_request.created_by:
            executed_by_share = commission * 0.4
            publisher_share = commission * 0.4
            platform_share = commission * 0.2

        Deal.objects.create(
            request=real_request,
            executed_by=request.user,
            publisher=real_request.created_by,
            amount=amount,
            commission=commission,
            platform_share=platform_share
        )

        real_request.status = 'contacted'
        real_request.save()

        messages.success(request, "✅ تم تنفيذ الطلب وتحويله إلى صفقة.")
        return redirect('requests:agent_my_requests')

    return render(request, 'requests/agent/execute.html', {'request_obj': real_request})


@login_required
@user_passes_test(lambda u: u.role == 'agent')
def my_deals_view(request):
    deals = Deal.objects.filter(executed_by=request.user).order_by('-created_at')
    return render(request, 'requests/agent/my_deals.html', {'deals': deals})

@login_required
def reserve_request(request, request_id):
    real_request = get_object_or_404(RealEstateRequest, id=request_id)

    if real_request.is_reserved:
        messages.error(request, "❌ تم حجز هذا الطلب من قبل وسيط آخر.")
        return redirect('requests:list')

    real_request.is_reserved = True
    real_request.reserved_by = request.user
    real_request.save()
    
    messages.success(request, "✅ تم حجز الطلب بنجاح.")
    return redirect('requests:list')

@login_required
def request_list(request):
    requests = RealEstateRequest.objects.all().order_by('-created_at')
    return render(request, 'requests/request_list.html', {'requests': requests})