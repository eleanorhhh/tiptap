from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')), # 統一交給 core.urls 處理
    path('', TemplateView.as_view(template_name='index.html')), 
]