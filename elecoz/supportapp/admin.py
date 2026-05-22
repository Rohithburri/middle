from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import SupportTicket


class SupportTicketResource(resources.ModelResource):
    class Meta:
        model = SupportTicket


@admin.register(SupportTicket)
class SupportTicketAdmin(ImportExportModelAdmin):
    resource_class = SupportTicketResource

    list_display = (
        'id',
        'name',
        'email',
        'issue_type',
        'transaction_id',
        'created_at'
    )

    search_fields = ('name', 'email', 'transaction_id')
    list_filter = ('issue_type', 'created_at')