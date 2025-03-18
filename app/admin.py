"""Django admin configuration."""
from django.contrib import admin

from .models import Table, User, Reservation, MenuItem, Order, OrderItem

# Register your models here.
admin.site.register(Table)
admin.site.register(User)
admin.site.register(Reservation)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(OrderItem)
