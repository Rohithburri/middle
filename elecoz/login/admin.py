from django.contrib import admin
from .models import User,B2BRequest,Cart

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'mobile', 'password']
    search_fields = ['id','name', 'email', 'mobile', 'password']



@admin.register(B2BRequest)
class B2BRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'company_name', 'gst_number', 'industry', 'status', 'created_at')
    list_filter = ('status', 'industry')
    search_fields = ('company_name', 'gst_number', 'user__username')




@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product_id','image', 'title', 'price', 'quantity')
    list_filter = ('user',)
    search_fields = ('title',)