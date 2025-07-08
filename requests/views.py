from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from .models import RealEstateRequest
from .models import RealEstateRequest
from .forms import RealEstateRequestForm, RealEstateRequestStatusForm
from properties.models import Property
from notifications.models import Notification
from django.db.models import Sum
from decimal import Decimal

  # تأكد من الاستيراد
from django.db.models import Exists, OuterRef
from deals.models import Deal
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from properties.forms import PropertyForm
from properties.models import Property
from django.utils.timezone import now

# ===== Helpers =====

def is_agent(user):
    return user.is_authenticated and getattr(user, 'role', None) == 'agent'


# ===== إدارة المشرف (Admin) =====

@staff_member_required
def admin_request_list(request):
    """عرض جميع طلبات العقار مع فلترة الحالة."""
    status_filter = request.GET.get('status')
    if status_filter:
        requests_qs = RealEstateRequest.objects.filter(status=status_filter)
    else:
        requests_qs = RealEstateRequest.objects.all()
    requests_qs = requests_qs.order_by('-created_at')
    return render(request, 'requests/admin/list.html', {'requests': requests_qs})


@staff_member_required
def admin_request_detail(request, pk):
    """تفاصيل طلب عقاري وإمكانية تحديث الحالة."""
    real_request = get_object_or_404(RealEstateRequest, pk=pk)
    old_status = real_request.status

    if request.method == 'POST':
        form = RealEstateRequestStatusForm(request.POST, instance=real_request)
        if form.is_valid():
            form.save()

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
@require_POST
def mark_request_as_reviewed(request, pk):
    """تغيير حالة الطلب إلى 'تمت المراجعة'."""
    req = get_object_or_404(RealEstateRequest, pk=pk)
    if req.status == 'new':
        req.status = 'reviewed'
        req.save()
    return redirect('requests:admin_detail', pk=pk)


@staff_member_required
@require_POST
def mark_request_as_contacted(request, pk):
    """تغيير حالة الطلب إلى 'تم التواصل' مع إرسال إشعار للمشرفين الآخرين."""
    req = get_object_or_404(RealEstateRequest, pk=pk)
    if req.status == 'reviewed':
        req.status = 'contacted'
        req.save()

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
@require_POST
def admin_request_delete(request, pk):
    """حذف طلب عقاري."""
    request_obj = get_object_or_404(RealEstateRequest, pk=pk)
    request_obj.delete()
    messages.success(request, "تم حذف الطلب بنجاح.")
    return redirect('requests:admin_list')


# ===== إنشاء الطلبات =====

def create_request(request, property_id):
    """إنشاء طلب جديد مرتبط بعقار معين."""
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
    """إنشاء طلب عام من زائر."""
    if request.method == 'POST':
        form = RealEstateRequestForm(request.POST)
        if form.is_valid():
            real_request = form.save()

            User = get_user_model()
            admins = User.objects.filter(is_superuser=True)
            for admin in admins:
                Notification.objects.create(
                    recipient=admin,
                    title="📩 طلب عقاري جديد",
                    message=f"تم إرسال طلب جديد من الزائر ({real_request.full_name}) برقم: {real_request.phone_number}",
                )

            messages.success(request, "✅ تم إرسال الطلب بنجاح، سنقوم بالتواصل معك قريبًا.")
            return redirect('home')
    else:
        form = RealEstateRequestForm()
    
    return render(request, 'requests/general_request.html', {'form': form})


# ===== واجهة الوسيط (Agent) =====
@user_passes_test(lambda u: u.is_authenticated and u.role == 'agent')

@login_required
@user_passes_test(is_agent)
def available_requests_for_agent(request):
    """عرض الطلبات المتاحة للوسيط (حالة مراجعة وغير محجوزة)."""
    requests = RealEstateRequest.objects.filter(
        status='reviewed',
        reserved_by__isnull=True
    )
    return render(request, 'requests/agent/available_requests.html', {
        'requests': requests
    })

@user_passes_test(lambda u: u.is_authenticated and u.role == 'agent')

@login_required
@user_passes_test(is_agent)
def reserve_request(request, pk):
    """حجز طلب متاح للوسيط."""
    real_request = get_object_or_404(RealEstateRequest, pk=pk, reserved_by__isnull=True)

    if request.method == 'POST':
        real_request.reserved_by = request.user
        real_request.save()
        messages.success(request, "✅ تم حجز الطلب بنجاح.")
        return redirect('requests:agent_available')

    return render(request, 'requests/agent/confirm_reserve.html', {
        'request_obj': real_request
    })

@user_passes_test(lambda u: u.is_authenticated and u.role == 'agent')

@login_required
@user_passes_test(is_agent)
def my_reserved_requests(request):
    """عرض الطلبات التي حجزها الوسيط."""
    requests = RealEstateRequest.objects.filter(reserved_by=request.user)
    return render(request, 'requests/agent/reserved_requests.html', {'requests': requests})



@login_required
@user_passes_test(is_agent)
def cancel_reservation(request, pk):
    """إلغاء حجز طلب من قبل الوسيط."""
    real_request = get_object_or_404(RealEstateRequest, pk=pk, reserved_by=request.user)

    if request.method == 'POST':
        real_request.reserved_by = None
        real_request.save()
        messages.success(request, "✅ تم إلغاء حجز الطلب بنجاح.")
        return redirect('requests:reserved_requests')

    return render(request, 'requests/agent/confirm_cancel.html', {
        'request_obj': real_request
    })


from django.db import IntegrityError
from deals.models import Deal

@user_passes_test(lambda u: u.is_authenticated and u.role == 'agent')


@login_required
@user_passes_test(is_agent)
def execute_request(request, pk):
    """تنفيذ الطلب وتحويله إلى صفقة مع حساب العمولة."""
    real_request = get_object_or_404(RealEstateRequest, pk=pk, reserved_by=request.user)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            messages.error(request, "❌ المبلغ غير صالح.")
            return redirect('requests:reserved_requests')

        # ✅ تحقق من عدم وجود صفقة سابقة
        if Deal.objects.filter(request=real_request).exists():
            messages.warning(request, "⚠️ تم تنفيذ الصفقة لهذا الطلب مسبقًا.")
            return redirect('requests:reserved_requests')

        # ✅ حساب العمولات
        commission = amount * 0.025
        executed_by_share = commission * 0.8
        publisher_share = 0.0
        platform_share = commission * 0.2

        if real_request.reserved_by != getattr(real_request, 'created_by', None) and getattr(real_request, 'created_by', None):
            executed_by_share = commission * 0.4
            publisher_share = commission * 0.4
            platform_share = commission * 0.2

        try:
            Deal.objects.create(
                request=real_request,
                executed_by=request.user,
                publisher=getattr(real_request, 'created_by', None),
                amount=amount,
                commission=commission,
                platform_share=platform_share
            )

            real_request.status = 'contacted'
            real_request.save()

            messages.success(request, "✅ تم تنفيذ الطلب وتحويله إلى صفقة.")
        except IntegrityError:
            messages.error(request, "❌ حدث خطأ أثناء إنشاء الصفقة، ربما تم إنشاؤها بالفعل.")
        
        return redirect('requests:reserved_requests')

    return render(request, 'requests/agent/execute.html', {'request_obj': real_request})


@user_passes_test(lambda u: u.is_authenticated and u.role == 'agent')

@login_required
@user_passes_test(is_agent)
def my_deals_view(request):
    deals = Deal.objects.filter(executed_by=request.user).select_related('request')
    for deal in deals:
        if deal.publisher:
            deal.agent_share = deal.commission * Decimal('0.4')
            deal.share_percent = "40٪"
        else:
            deal.agent_share = deal.commission * Decimal('0.8')
            deal.share_percent = "80٪"
    return render(request, 'requests/agent/my_deals.html', {'deals': deals})




# ===== دوال عامة (إن وجدت) =====

@login_required
def request_list(request):
    """عرض كل الطلبات - غير مقيد بدور."""
    requests = RealEstateRequest.objects.all().order_by('-created_at')
    return render(request, 'requests/request_list.html', {'requests': requests})


@login_required
def broker_request_list(request):
    """عرض الطلبات للوسيط مع تحقق من الدور."""
    if request.user.role != 'agent':
        return render(request, 'errors/403.html', status=403)

    requests = RealEstateRequest.objects.all().order_by('-created_at')

    return render(request, 'requests/broker_request_list.html', {'requests': requests})

@login_required
def reserved_requests_for_agent(request):
    if request.user.role != 'agent':
        return render(request, 'accounts/unauthorized.html', status=403)

    reserved_qs = RealEstateRequest.objects.annotate(
        has_deal=Exists(Deal.objects.filter(request=OuterRef('pk')))
    ).filter(
        reserved_by=request.user
    ).select_related('reserved_by').order_by('-created_at')

    context = {
        'requests': reserved_qs,
    }
    return render(request, 'requests/agent/reserved_requests.html', context)

    reserved_qs = RealEstateRequest.objects.filter(
        reserved_by=request.user
    ).select_related('reserved_by').select_related('deal').order_by('-created_at')

    context = {
        'requests': reserved_qs,
    }
    return render(request, 'requests/agent/reserved_requests.html', context)



@login_required
def cancel_reservation(request, request_id):
    real_estate_request = get_object_or_404(
        RealEstateRequest,
        id=request_id,
        reserved_by=request.user
    )

    if request.method == "POST":
        real_estate_request.reserved_by = None
        real_estate_request.save()
        messages.success(request, "تم إلغاء حجز الطلب.")
        return redirect('requests:reserved_requests')
    
    return render(request, 'requests/agent/confirm_cancel.html', {'request_obj': real_estate_request})

# شرط التحقق من كون المستخدم وسيط
def is_agent(user):
    return user.is_authenticated and user.role == 'agent'

from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import RealEstateRequest
from deals.models import Deal


@login_required
def agent_dashboard_view(request):
    agent = request.user

    # الطلبات المحجوزة (محجوزة من قبل الوسيط الحالي ولم يتم تنفيذ صفقة لها)
    reserved_requests = RealEstateRequest.objects.filter(
        reserved_by=agent,
        deal__isnull=True
    )

    # الطلبات المنفذة (يوجد صفقة مرتبطة بها وتم تنفيذها بواسطة نفس الوسيط)
    executed_requests = Deal.objects.filter(executed_by=agent)

    total_reserved = reserved_requests.count()
    total_executed = executed_requests.count()
    total_deals_amount = executed_requests.aggregate(Sum('amount'))['amount__sum'] or 0
    total_commission = executed_requests.aggregate(Sum('commission'))['commission__sum'] or 0

    context = {
        'total_reserved': total_reserved,
        'total_executed': total_executed,
        'total_deals_amount': total_deals_amount,
        'total_commission': total_commission,
        'now': timezone.now(),
    }

    return render(request, 'requests/agent/dashboard.html', context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import RealEstateRequest
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from .models import RealEstateRequest
 
@login_required
@user_passes_test(is_agent)
def agent_available_requests_view(request):
    """
    عرض الطلبات المتاحة للوسيط العقاري (المعتمدة فقط - لم يتم حجزها أو تنفيذها - وتم التواصل مع العميل)
    مع دعم فلترة حسب نوع الطلب (purchase/rent/...).
    """
    purpose = request.GET.get('purpose')  # استرجاع الفلتر من الرابط

    available_requests = RealEstateRequest.objects.filter(
        is_approved=True,
        reserved_by__isnull=True,
        deal__isnull=True,
        status='contacted'
    )

    if purpose:
        available_requests = available_requests.filter(purpose=purpose)

    available_requests = available_requests.order_by('-created_at')

    context = {
        'requests': available_requests,
        'selected_purpose': purpose or '',  # تمرير القيمة المختارة للقالب
    }

    return render(request, 'requests/agent/available_requests.html', context)


# views.py
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
@require_POST
def approve_request(request, request_id):
    req = get_object_or_404(RealEstateRequest, id=request_id)
    req.is_approved = True
    req.save()
    messages.success(request, "تمت الموافقة على الطلب بنجاح.")
    return redirect('requests:admin_list')
# views.py في عرض الوسطاء
def available_requests(request):
    requests = RealEstateRequest.objects.filter(
        is_approved=True,
        reserved_by__isnull=True
    )
    ...
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from properties.forms import PropertyForm
from properties.models import Property

# ✅ دالة تحقق الوسيط
def is_agent(user):
    return user.is_authenticated and user.role == 'agent'


@login_required
def agent_add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.created_by = request.user
            property.status = 'pending'  # أو أي حالة تمثل "قيد المراجعة"
            property.save()
            messages.success(request, "✅ تمت إضافة العقار بنجاح، وهو الآن تحت مراجعة الإدارة لاعتماده.")
            return redirect('requests:agent_dashboard')  # أو صفحة النجاح
    else:
        form = PropertyForm()
    return render(request, 'requests/agent/add_property.html', {'form': form})


# requests/views.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect
from .models import RealEstateRequest

# فقط للمشرفين
def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@login_required
@user_passes_test(is_admin)
def admin_approve_request(request, pk):
    req = get_object_or_404(RealEstateRequest, pk=pk)
    req.is_approved = True
    req.save()
    messages.success(request, "تم اعتماد الطلب بنجاح.")
    return redirect('requests:admin_list')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import RealEstateRequest

@login_required
def available_requests_for_agents(request):
    if not request.user.is_authenticated or not request.user.role == 'agent':
        return render(request, 'accounts/unauthorized.html', status=403)

    requests_qs = RealEstateRequest.objects.filter(
        is_approved=True,
        reserved_by__isnull=True  # الطلب غير محجوز بعد
    ).order_by('-created_at')

    context = {
        'requests': requests_qs,
    }
    return render(request, 'requests/agent/available_requests.html', context)

@login_required
def available_requests_for_agents(request):
    if request.user.role != 'agent':
        return render(request, 'accounts/unauthorized.html', status=403)

    requests_qs = RealEstateRequest.objects.filter(
        is_approved=True,
        reserved_by__isnull=True
    ).order_by('-created_at')

    context = {
        'requests': requests_qs,
    }
    return render(request, 'requests/agent/available_requests.html', context)

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

@login_required
def confirm_reserve_request(request, request_id):
    real_estate_request = get_object_or_404(
        RealEstateRequest,
        id=request_id,
        is_approved=True,
        reserved_by__isnull=True
    )

    if request.method == "POST":
        real_estate_request.reserved_by = request.user
        real_estate_request.save()
        messages.success(request, "تم حجز الطلب بنجاح.")
        return redirect('requests:reserved_requests')  # أو الصفحة التي تريد التوجيه إليها بعد الحجز

    context = {
        'request_obj': real_estate_request
    }
    return render(request, 'requests/agent/confirm_reserve.html', context)

@login_required
def execute_deal(request, request_id):
    real_estate_request = get_object_or_404(
        RealEstateRequest,
        id=request_id,
        reserved_by=request.user
    )

    # تحقق إذا كانت الصفقة موجودة مسبقًا (اختياري)
    if request.method == 'POST':
        # منطق إنشاء الصفقة (بشكل مبدئي):
        Deal.objects.create(
            agent=request.user,
            real_estate_request=real_estate_request,
            amount=real_estate_request.budget or 0,
            status='pending'  # أو أي قيمة افتراضية
        )
        messages.success(request, 'تم تسجيل الصفقة بنجاح.')
        return redirect('requests:reserved_requests')

    return render(request, 'requests/agent/execute.html', {'request_obj': real_estate_request})

def is_agent(user):
    return user.is_authenticated and user.role == 'agent'


@login_required
def agent_reserved_requests_view(request):
    """عرض الطلبات التي قام الوسيط بحجزها ولم تُنفذ بعد."""
    agent = request.user
    reserved_requests = RealEstateRequest.objects.filter(
        reserved_by=agent,
        deal__isnull=True
    ).order_by('-reserved_at')

    context = {
        'requests': reserved_requests
    }
    return render(request, 'requests/agent/reserved_requests.html', context)


@staff_member_required
def admin_list(request):
    requests = RealEstateRequest.objects.all().order_by('-created_at')
    return render(request, 'requests/admin_list.html', {'requests': requests})
