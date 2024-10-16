from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(PassItem)
admin.site.register(PassOrder)
admin.site.register(PassOrderItems)