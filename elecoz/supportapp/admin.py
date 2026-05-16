from django.contrib import admin
from .models import SupportTicket

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
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