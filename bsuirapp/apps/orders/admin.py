from django.contrib import admin
from .models import Order, OrderItem
from .email_procedure import send_verify_emails

def send_remainder(model_admin, request, queryset):
    for order in queryset:
        send_verify_emails(order, request)


# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
    'address', 'postal_code', 'city', 'paid', 'verified',
    'created', 'updated']
    list_filter = ['paid', 'verified', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [send_remainder]