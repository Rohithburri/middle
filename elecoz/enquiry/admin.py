# from django.contrib import admin
# from .models import Enquiry


# class EnquiryAdmin(admin.ModelAdmin):
#     list_display = [
#         'id',
#         'user_id',
#         'title',
#         'product_id',
#         'quantity',
#         'price',
#         'created_at'
#     ]

#     list_filter = [
#         'created_at'
#     ]

#     search_fields = [
#         'title',
#         'code',
#         'brand',
#         'user_id'
#     ]


# admin.site.register(Enquiry, EnquiryAdmin)

from django.contrib import admin
from .models import Enquiry


# class EnquiryAdmin(admin.ModelAdmin):
#     list_display = [
#         'id',
#         'user_id',
#         'title',
#         'product_id',
#         'quantity',
#         'price',
#         'status',
#         'created_at'
#     ]

#     list_filter = [
#         'status',
#         'created_at'
#     ]

#     search_fields = [
#         'title',
#         'code',
#         'brand',
#         'user_id'
#     ]

#     ordering = ['-id']

#     # 🔥 OPTIONAL (edit status directly in list)
#     list_editable = ['status']


# admin.site.register(Enquiry, EnquiryAdmin)

from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Enquiry


class EnquiryResource(resources.ModelResource):
    class Meta:
        model = Enquiry


@admin.register(Enquiry)
class EnquiryAdmin(ImportExportModelAdmin):
    resource_class = EnquiryResource

    list_display = [
        'id',
        'user_id',
        'image',
        'title',
        'product_id',
        'quantity',
        'price',
        'status',
        'created_at'
    ]

    list_filter = ['status', 'created_at']

    search_fields = ['title', 'code', 'brand', 'user_id__exact']

    ordering = ['-id']

    list_editable = ['status']

    readonly_fields = ['created_at']

    date_hierarchy = 'created_at'