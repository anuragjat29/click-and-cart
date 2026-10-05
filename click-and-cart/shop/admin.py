from django.contrib import admin

# Register your models here.
from .models import product
admin.site.register(product)

from .models import contact
admin.site.register(contact)

from .models import orders, orderitems, orderupdate
admin.site.register(orders)
admin.site.register(orderitems)
admin.site.register(orderupdate)