"""
URL configuration for larin_a_iu5 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path

from lab import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.GetPasses),
    path('pass_url/<int:selected_id>', views.GetPass, name='pass_url'),
    path('cart/<int:id>', views.GetCart, name='pass_cart'),
    path('add_to_order/', views.AddPassItem),
    path('pass_cart/<int:selected_id>/del_order/', views.DelPassItem, name='del_order')
]
