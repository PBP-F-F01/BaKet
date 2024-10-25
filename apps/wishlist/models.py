from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth.models import User
from apps.catalogue.models import Product

# Create your models here.
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlist_items')
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'product'], name='unique_user_product_wishlist')
        ]
        verbose_name = 'Wishlist'
        verbose_name_plural = 'Wishlists'
        ordering = ['-added_on']

    def __str__(self):
        return f'{self.user.username} - {self.product.name}'