from .models import News  # تأكد أن لديك نموذج الأخبار News

def news_ticker(request):
    news_items = News.objects.filter(is_active=True).order_by('-created_at')
    return {'news_ticker_items': news_items}
