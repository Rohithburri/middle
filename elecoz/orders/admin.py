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
from .models import Order, OrderItem, Wishlist


# 🔹 INLINE: Show order items inside Order
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


# 🔹 ORDER ADMIN
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
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

    # 🔥 Show total quantity of items
    def total_items(self, obj):
        return sum(item.qty for item in obj.items.all())

    total_items.short_description = "Items"


# 🔹 ORDER ITEM ADMIN
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'title', 'price', 'qty']
    search_fields = ['title']
    ordering = ['-id']


# 🔹 WISHLIST ADMIN
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'title','image', 'price', 'created_at']
    search_fields = ['title', 'user_id__exact']
    ordering = ['-id']
    readonly_fields = ['created_at']



from .models import Address


# 🔹 ADDRESS ADMIN (PROPER)
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
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


# admin.py
from django.contrib import admin
from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "message", "created_at")
    search_fields = ("name", "email", "message")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

admin.site.register(Contact, ContactAdmin)