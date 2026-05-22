# from django.contrib import admin
# from .models import Order, OrderItem


# # 🔹 OrderItem inline (shows items inside order)
# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     extra = 0


# # 🔹 Order Admin
# class OrderAdmin(admin.ModelAdmin):
#     list_display = [
#         'id',
#         'user_id',
#         'total',
#         'status',
#         'payment_id',   # ✅ ADD THIS
#         'created_at'
#     ]

#     list_filter = [
#         'status',
#         'created_at'
#     ]

#     search_fields = [
#         'id',
#         'user_id',
#         'payment_id'   # ✅ ADD THIS
#     ]

#     inlines = [OrderItemInline]


# # 🔹 Register models
# admin.site.register(Order, OrderAdmin)
# admin.site.register(OrderItem)



from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Order, OrderItem, Wishlist, Address


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderResource(resources.ModelResource):
    class Meta:
        model = Order


@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin):
    resource_class = OrderResource

    list_display = [
        'id',
        'user_id',
        'total',
        'total_items',
        'address',
        'status',
        'payment_id',
        'created_at'
    ]

    list_filter = [
        'status',
        'created_at'
    ]

    search_fields = [
        'id__exact',
        'user_id__exact',
        'payment_id'
    ]

    ordering = ['-id']

    inlines = [OrderItemInline]

    readonly_fields = ['created_at']

    date_hierarchy = 'created_at'

    def total_items(self, obj):
        return sum(item.qty for item in obj.items.all())

    total_items.short_description = "Items"


class OrderItemResource(resources.ModelResource):
    class Meta:
        model = OrderItem


@admin.register(OrderItem)
class OrderItemAdmin(ImportExportModelAdmin):
    resource_class = OrderItemResource

    list_display = ['id', 'order', 'title', 'price', 'qty']
    search_fields = ['title']
    ordering = ['-id']


class WishlistResource(resources.ModelResource):
    class Meta:
        model = Wishlist


@admin.register(Wishlist)
class WishlistAdmin(ImportExportModelAdmin):
    resource_class = WishlistResource

    list_display = ['id', 'user_id', 'title', 'image', 'price', 'created_at']
    search_fields = ['title', 'user_id__exact']
    ordering = ['-id']
    readonly_fields = ['created_at']


class AddressResource(resources.ModelResource):
    class Meta:
        model = Address


@admin.register(Address)
class AddressAdmin(ImportExportModelAdmin):
    resource_class = AddressResource

    list_display = [
        "id",
        "user_id",
        "full_name",
        "phone",
        "city",
        "state",
        "pincode",
        "created_at",
    ]

    list_filter = [
        "state",
        "city",
        "created_at",
    ]

    search_fields = [
        "full_name",
        "phone",
        "email",
        "city",
        "pincode",
        "user_id",
    ]

    ordering = ["-created_at"]

    readonly_fields = ["created_at"]