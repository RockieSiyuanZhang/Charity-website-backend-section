from django.contrib import admin

# Register your models here.

from .models import Recipient, Donor, Order, Stock, Donation, Kit, ItemCategory, OrderItem, Size, Item, OrderKit


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderKitInline(admin.TabularInline):
    model = OrderKit
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline, OrderKitInline]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
        formset.save_m2m()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()
        queryset.delete()

# class KitItemInline(admin.TabularInline):
#     model=KitItem
#     extra = 5

class KitAdmin(admin.ModelAdmin):
    filter_horizontal = ('item',)


admin.site.register(Recipient)
admin.site.register(Donor)
admin.site.register(Order, OrderAdmin)
admin.site.register(Item)
admin.site.register(Stock)
admin.site.register(Donation)
admin.site.register(Kit, KitAdmin)
admin.site.register(OrderKit)
admin.site.register(ItemCategory)
admin.site.register(OrderItem)
admin.site.register(Size)
