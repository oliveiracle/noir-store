from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemInline,)
    readonly_fields = (
        'order_number', 'date', 'delivery_cost',
        'order_total', 'grand_total',
    )
    list_display = (
        'order_number', 'date', 'full_name', 'grand_total',
    )
    ordering = ('-date',)
