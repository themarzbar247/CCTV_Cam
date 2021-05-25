from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Alert)
admin.site.register(Notification)
admin.site.register(Type)