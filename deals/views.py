# deals/views.py
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import Deal
from django.shortcuts import render, get_object_or_404, redirect
from requests.models import RealEstateRequest


# ✅ عرض الصفقات للمشرف
@staff_member_required
def admin_deals_view(request):
    deals = Deal.objects.select_related(
        'request',               # الطلب العقاري
        'request__reserved_by', # العميل
        'executed_by',          # الوسيط
    ).all()

    context = {
        'deals': deals,
    }
    return render(request, 'deals/admin_deals.html', context)


# ✅ عرض صفقات الوسيط
@login_required
def agent_deals_view(request):
    deals = Deal.objects.filter(executed_by=request.user).select_related('request').order_by('-created_at')
    return render(request, 'deals/agent_deals.html', {'deals': deals})

from django.utils import timezone

@login_required
def create_deal_view(request, request_id):
    real_estate_request = get_object_or_404(RealEstateRequest, id=request_id)

    # التأكد من أن المستخدم هو المنفذ
    if request.user != real_estate_request.executed_by:
        return redirect('requests:agent_reserved')

    # إنشاء الصفقة إن لم تكن موجودة
    if not Deal.objects.filter(request=real_estate_request).exists():
        Deal.objects.create(
            request=real_estate_request,
            executed_by=request.user,
            commission=real_estate_request.suggested_commission or 0,
            platform_share=real_estate_request.suggested_platform_share or 0
        )

        # ✅ تحديث حالة الطلب
        real_estate_request.status = 'executed'
        real_estate_request.save()

    return redirect('requests:agent_reserved')
