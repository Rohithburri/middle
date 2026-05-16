from django.db import models

class SupportTicket(models.Model):
    ISSUE_TYPES = [
        ('Payment Issue', 'Payment Issue'),
        ('Other Issue', 'Other Issue'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    issue_type = models.CharField(max_length=50, choices=ISSUE_TYPES)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name