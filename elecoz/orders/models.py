from django.db import models
# 🔹 ORDER MODEL
class Order(models.Model):
    user_id = models.IntegerField()
    total = models.FloatField()

    address = models.ForeignKey(
        'Address',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ("Pending", "Pending"),
            ("Processing", "Processing"),
            ("Completed", "Completed"),
            ("Failed", "Failed"),
        ],
        default="Pending"
    )

    payment_id = models.CharField(max_length=255, null=True, blank=True)

    # Add these for Razorpay verification
    razorpay_order_id = models.CharField(max_length=255, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)

    # Add these for invoice email
    invoice_sent = models.BooleanField(default=False)
    invoice_sent_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - User {self.user_id}"


# 🔹 ORDER ITEM MODEL
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'   # ✅ important for API
    )
    product_id = models.IntegerField()
    title = models.CharField(max_length=255)
    image = models.TextField(blank=True, null=True)
    price = models.FloatField()
    qty = models.IntegerField()

    def __str__(self):
        return f"{self.title} ({self.qty})"

#wishlist
class Wishlist(models.Model):
    user_id = models.IntegerField()

    product_id = models.IntegerField()
    image = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=100, null=True, blank=True)
    brand = models.CharField(max_length=100, null=True, blank=True)

    price = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)




# 🔹 ADDRESS MODEL
class Address(models.Model):
    user_id = models.IntegerField()

    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email = models.EmailField()

    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)

    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    country = models.CharField(max_length=50, default="India")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


from django.db import models

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=10)

    def __str__(self):
        return self.name

from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name