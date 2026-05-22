from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import User, B2BRequest, Cart


class UserResource(resources.ModelResource):
    class Meta:
        model = User


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource

    list_display = ['id', 'name', 'email', 'mobile', 'password']
    search_fields = ['id', 'name', 'email', 'mobile', 'password']


class B2BRequestResource(resources.ModelResource):
    class Meta:
        model = B2BRequest


@admin.register(B2BRequest)
class B2BRequestAdmin(ImportExportModelAdmin):
    resource_class = B2BRequestResource

    list_display = ('id', 'user', 'company_name', 'gst_number', 'industry', 'status', 'created_at')
    list_filter = ('status', 'industry')
    search_fields = ('company_name', 'gst_number', 'user__username')


class CartResource(resources.ModelResource):
    class Meta:
        model = Cart


@admin.register(Cart)
class CartAdmin(ImportExportModelAdmin):
    resource_class = CartResource

    list_display = ('id', 'user', 'product_id', 'image', 'title', 'price', 'quantity')
    list_filter = ('user',)
    search_fields = ('title',)