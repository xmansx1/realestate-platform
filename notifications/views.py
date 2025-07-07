from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification

@staff_member_required
def notification_list(request):
    """
    عرض قائمة التنبيهات للمشرف الحالي.
    """
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, 'notifications/list.html', {
        'notifications': notifications
    })

@staff_member_required
def mark_notification_read(request, pk):
    """
    تمييز تنبيه معين كمقروء.
    """
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications:notification_list')

@staff_member_required
def mark_all_read(request):
    """
    تمييز كل التنبيهات كمقروءة.
    """
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return redirect('notifications:notification_list')
