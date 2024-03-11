from django.contrib import admin
from .models import Record
from .models import Drug
from .models import Order

admin.site.register(Record)
admin.site.register(Drug)
admin.site.register(Order)