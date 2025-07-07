from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from properties.models import Property
from requests.models import RealEstateRequest
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Count, Sum
from requests.models import Deal, RealEstateRequest


@staff_member_required
def dashboard_view(request):
    total_requests = RealEstateRequest.objects.count()
    new_requests = RealEstateRequest.objects.filter(status='new').count()

    total_properties = Property.objects.count()
    active_properties = Property.objects.filter(status='active').count()
    archived_properties = Property.objects.filter(status='archived').count()

    context = {
        'total_requests': total_requests,
        'new_requests': new_requests,
        'total_properties': total_properties,
        'active_properties': active_properties,
        'archived_properties': archived_properties,
    }
    return render(request, 'dashboard/dashboard.html', context)

@staff_member_required
def admin_dashboard_view(request):
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    filters = {}

    if start_date:
        filters['created_at__gte'] = start_date
    if end_date:
        filters['created_at__lte'] = end_date

    deals = Deal.objects.filter(**filters)

    stats = {
        'total_requests': RealEstateRequest.objects.count(),
        'requests_by_status': RealEstateRequest.objects.values('status').annotate(total=Count('id')),
        'total_deals': deals.count(),
        'total_commission': deals.aggregate(total=Sum('commission'))['total'] or 0,
        'platform_share': deals.aggregate(total=Sum('platform_share'))['total'] or 0,
    }

    return render(request, 'admin_dashboard.html', {
        'stats': stats,
        'start_date': start_date,
        'end_date': end_date,
    })
    
# dashboard/views.py

import datetime
import openpyxl
from django.http import HttpResponse
from requests.models import Deal

def export_deals_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Deals Report"

    headers = ["ID", "التاريخ", "الطلب", "القيمة", "العمولة", "المنفذ", "الناشر", "حصة المنصة"]
    ws.append(headers)

    for deal in Deal.objects.all():
        ws.append([
            deal.id,
            deal.created_at.strftime("%Y-%m-%d"),
            str(deal.request),
            deal.value,
            deal.commission,
            str(deal.agent_executor),
            str(deal.agent_publisher),
            deal.platform_share,
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    filename = f"deals_report_{datetime.date.today()}.xlsx"
    response['Content-Disposition'] = f'attachment; filename={filename}'
    wb.save(response)
    return response
