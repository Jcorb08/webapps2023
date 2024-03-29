"""webapps2023 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, register_converter
from register import views as register_views
from payapp import views as payapp_views
from api import views as api_views
from api import converter

register_converter(converter.DecimalConverter, 'decimal')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', payapp_views.home, name="home"),
    path('register/', register_views.register_user, name='register'),
    path('login/', register_views.login_user, name='login'),
    path('logout/', register_views.logout_user, name='logout'),
    path('request/', payapp_views.payment, name='request'),
    path('send/', payapp_views.payment, name='send'),
    path('conversion/<str:currency_from>/<str:currency_to>/<decimal:amount>',
         api_views.Conversion.as_view(), name='conversion_amount'),
    path('conversion/<str:currency_from>/<str:currency_to>',
         api_views.Conversion.as_view(), name='conversion_rate')
]
