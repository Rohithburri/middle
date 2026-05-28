from django.db import models

class Category(models.Model):
    # name = models.CharField(max_length=100)
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="categories/", null=True, blank=True)

    def __str__(self):
        return self.name


from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="categories/", null=True, blank=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories"
    )
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="subcategories/", null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        unique_together = ("category", "name")
        verbose_name_plural = "Sub Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.category.name}-{self.name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} - {self.name}"


from django.utils.text import slugify

class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    # code = models.CharField(max_length=200, blank=True)
    code = models.CharField(max_length=200, unique=True)

    price = models.FloatField()
    old_price = models.FloatField(null=True, blank=True)
    discount = models.CharField(max_length=50, blank=True)

    ampere = models.CharField(max_length=50, blank=True)
    poles = models.CharField(max_length=50, blank=True)
    breaking_capacity = models.CharField(max_length=50, blank=True)
    setting_type = models.CharField(max_length=50, blank=True)

    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image2 = models.ImageField(upload_to='products/', null=True, blank=True)
    pdf = models.FileField(upload_to='pdfs/', blank=True, null=True)

    auxiliary_contact = models.CharField(max_length=100, blank=True, null=True)

    coil_voltage = models.CharField(max_length=100, blank=True, null=True)

    duty = models.CharField(max_length=100, blank=True, null=True)

    stock_status = models.CharField(max_length=100, blank=True, null=True)

    dispatch_date = models.CharField(max_length=100, blank=True, null=True)

    warehouse = models.CharField(max_length=200, blank=True, null=True)

    quantity = models.IntegerField(default=0)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    # ✅ ADD THIS
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    def save(self, *args, **kwargs):
        if self.quantity <= 0:
            self.stock_status = "Out Of Stock"

        elif self.quantity <= 2:
            self.stock_status = "Limited Stock"

        else:
            self.stock_status = "In Stock"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


