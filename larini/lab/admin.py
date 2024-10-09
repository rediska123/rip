from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(PassItem)
admin.site.register(PassOrder)
admin.site.register(PassOrderItems)