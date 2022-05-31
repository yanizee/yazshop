from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Item)
admin.site.register(Beat)
admin.site.register(Pack)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Payment)