

# from django.contrib import admin
# from django.utils.html import format_html
# from .models import Product, Category, Brand


# # 🔹 CATEGORY ADMIN
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')
#     search_fields = ('name',)
#     ordering = ('name',)


# # 🔹 BRAND ADMIN
# @admin.register(Brand)
# class BrandAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'slug')
#     search_fields = ('name',)
#     ordering = ('name',)


# # 🔹 PRODUCT ADMIN
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'name',
#         'code',
#         'price',
#         'category',
#         'brand',
#         'pdf',
#         'image_preview'
#     )

#     search_fields = ('name', 'code')
#     list_filter = ('category', 'brand')
#     ordering = ('-id',)

#     fields = [
#         'name',
#         'code',
#         'price',
#         'old_price',
#         'discount',
#         'ampere',
#         'poles',
#         'breaking_capacity',
#         'setting_type',
#         'image',
#         'image2',
#            'pdf',
#         'category',
#         'brand'
#     ]

#     # 🔥 Make some fields optional in admin form
#     def get_form(self, request, obj=None, **kwargs):
#         form = super().get_form(request, obj, **kwargs)
#         form.base_fields['code'].required = False
#         form.base_fields['setting_type'].required = False
#         return form

#     # 🔥 Image preview in admin
#     # def image_preview(self, obj):
#     #     if obj.image:
#     #         return format_html('<img src="{}" width="50" />', obj.image.url)
#     #     return "-"
#     # image_preview.short_description = "Image"
#     def image_preview(self, obj):
#         if obj.image:
#             return format_html(
#                 '<a href="{}" target="_blank"><img src="{}" width="50" /></a>',
#                 obj.image.url,
#                 obj.image.url
#             )
#         return "-"




from django.contrib import admin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Product, Category, Brand, SubCategory


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


class SubCategoryResource(resources.ModelResource):
    class Meta:
        model = SubCategory


@admin.register(SubCategory)
class SubCategoryAdmin(ImportExportModelAdmin):
    resource_class = SubCategoryResource
    list_display = ('id', 'name', 'category', 'slug')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)
    ordering = ('category', 'name')


class BrandResource(resources.ModelResource):
    class Meta:
        model = Brand


@admin.register(Brand)
class BrandAdmin(ImportExportModelAdmin):
    resource_class = BrandResource
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    ordering = ('name',)


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource

    list_display = (
        'id', 'name', 'code', 'price',
        'category', 'subcategory', 'brand',
        'auxiliary_contact', 'coil_voltage', 'duty',
        'stock_status', 'dispatch_date', 'warehouse',
        'pdf', 'quantity', 'image_preview'
    )

    search_fields = ('name', 'code')
    list_filter = ('category', 'subcategory', 'brand')
    ordering = ('-id',)

    fields = [
        'name', 'code', 'price', 'old_price', 'discount',
        'ampere', 'poles', 'breaking_capacity', 'setting_type',
        'auxiliary_contact', 'coil_voltage', 'duty',
        'stock_status', 'dispatch_date', 'warehouse',
        'image', 'image2', 'pdf', 'quantity',
        'category', 'subcategory', 'brand'
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        for field in ['code', 'setting_type']:
            if field in form.base_fields:
                form.base_fields[field].required = False

        return form

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" width="50" /></a>',
                obj.image.url,
                obj.image.url
            )
        return "-"

    image_preview.short_description = "Image"