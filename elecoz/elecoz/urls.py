"""
URL configuration for elecoz project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import get_pincode

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('products.urls')),
    # ✅ LOGIN / REGISTER API (ADD THIS LINE)
    path('api/', include('login.urls')),
    path('api/', include('orders.urls')), #ORDERS
     path('api/', include('enquiry.urls')),  # ✅ ADD THIS
      path('api/', include('supportapp.urls')),
      path('api/pincode/<str:pincode>/', get_pincode),
     
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
