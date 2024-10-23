from django.db import models

# For filter feature
CATEGORY_CHOICES = [
    ('laptop', 'Laptop'),
    ('smart_watch', 'Smart Watch'),
    ('smart_tv', 'Smart TV'),
    ('handphone', 'Handphone'),
    ('tablet', 'Tablet'),
]

class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product_images/')
    price = models.IntegerField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name