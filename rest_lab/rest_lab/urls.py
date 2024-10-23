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

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Лабороторное оборудование API",
      default_version='v1',
      description="Апи для оформления закупок лабораторного оборудования",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@labeq.ru"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   #permission_classes=(permissions.AllowAny,),
)


router = routers.DefaultRouter()

urlpatterns = urlpatterns = [
    path('', include(router.urls)),
    path(r'passes/', views.pass_catalog.as_view(), name='pass-catalog'),
    path(r'client_cards/', views.pass_client_cards.as_view(), name='pass-client_cards'),
    path(r'passes/<int:id>/', views.pass_item.as_view(), name='pass-item'),
    path(r'passes/<int:id>/add', views.add_pass_to_client_card, name='add-pass-to-client_card'),
    path(r'client_cards/<int:id>/', views.pass_client_card.as_view(), name='pass-client_card'),
    path(r'client_cards/<int:id>/submit/', views.submit_client_card, name='submit-client_card'),
    path(r'client_cards/<int:id>/accept/', views.accept_client_card, name='accept-client_card'),
    path(r'client_card_pass/<int:id>/', views.pass_client_card_pass.as_view(), name='pass-client_card-item'),
    path(r'user/', views.user_registration, name='registration'),
    path(r'auth/', views.user_auth, name='auth'),
    path(r'logout/', views.user_deauth, name='logout'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
