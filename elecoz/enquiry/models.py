from django.db import models

class Enquiry(models.Model):
    user_id = models.IntegerField()

    product_id = models.IntegerField()
    image = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=100, null=True, blank=True)
    brand = models.CharField(max_length=100, null=True, blank=True)

    quantity = models.IntegerField()
    price = models.FloatField(null=True, blank=True)

    # ✅ ADD THIS
    status = models.CharField(
        max_length=20,
        choices=[
            ("Pending", "Pending"),
            ("Submitted", "Submitted"),
        ],
        default="Pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

