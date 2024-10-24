from django.contrib import admin
from .models import Review, Product

# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'rating', 'created_at']
    readonly_fields = ['created_at']