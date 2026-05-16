from django.db import models
class User(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.email

class B2BRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    company_name = models.CharField(max_length=255)
    gst_number = models.CharField(max_length=50)
    industry = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.IntegerField()
    title = models.CharField(max_length=255)
    image = models.TextField(blank=True, null=True)
    price = models.FloatField()
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.email} - {self.title}"