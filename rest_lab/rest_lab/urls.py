"""
URL configuration for rest_lab project.

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
from passes import views
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = urlpatterns = [
    path('', include(router.urls)),
    path(r'passes/', views.pass_catalog, name='pass-catalog'),
    path(r'orders/', views.pass_orders, name='pass-orders'),
    path(r'passes/<int:id>/', views.pass_item, name='pass-item'),
    path(r'passes/<int:id>/add', views.add_pass_to_order, name='add-pass-to-order'),
    path(r'orders/<int:id>/', views.pass_order, name='pass-order'),
    path(r'orders/<int:id>/submit/', views.submit_order, name='submit-order'),
    path(r'orders/<int:id>/accept/', views.accept_order, name='accept-order'),
    path(r'order_pass/<int:id>/', views.pass_order_item, name='pass-order-item'),
    path(r'user/', views.user_registration, name='registration'),
    path(r'auth/', views.user_auth, name='auth'),
    path(r'logout/', views.user_deauth, name='logout'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
