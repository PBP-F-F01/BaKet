from django.shortcuts import render
from .models import Product
from django.db.models import Q

def catalogue_view(request):
    products = Product.objects.all()
    query = request.GET.get('q')
    category_filter = request.GET.get('category')

    if query:
        products = products.filter(Q(name__icontains=query))
    
    if category_filter:
        products = products.filter(category=category_filter)

    return render(request, 'catalogue.html', {
        'products': products,
        'categories': Product.category
    })

def add_product(request):
    return render(request, 'add-product.html')
