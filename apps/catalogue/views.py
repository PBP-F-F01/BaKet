from django.shortcuts import get_object_or_404, render, redirect
from datetime import datetime
from django.http import HttpResponse
from apps.catalogue.models import Product, Review
from apps.catalogue.forms import ProductForm, ReviewForm

from django.shortcuts import render
from .models import Product

def catalogue_view(request):
    products = Product.objects.all()
    query = request.GET.get('q')
    categories = request.GET.getlist('category')
    sort_option = request.GET.get('sort')

    # Handle search
    if query:
        products = products.filter(name__icontains=query)

    # Handle filtering by category
    if categories:
        products = products.filter(category__in=categories)

    # Handle sorting
    if sort_option == 'price_asc':
        products = products.order_by('price')
    elif sort_option == 'price_desc':
        products = products.order_by('-price')

    context = {
        'products': products,
        'categories': Product.CATEGORY_CHOICES,  
        'selected_categories': categories,  
        'selected_sort': sort_option,
    }

    return render(request, 'catalogue.html', context)


def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalogue')  # Redirect after saving
    else:
        form = ProductForm()

    return render(request, 'add-product.html', {'form': form})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product).order_by('-created_at')  # Fetch all reviews for this product
    rating = Review.objects.filter(rating=0).order_by("?").first()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user  # Assuming you have user authentication set up
            review.save()
            return redirect('product_detail', product_id=product_id)  # Refresh the page after review submission
    else:
        form = ReviewForm()

    return render(request, 'details.html', {'product': product, 'reviews': reviews, 'form': form, 'rating': rating})