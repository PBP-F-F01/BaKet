from django.shortcuts import get_object_or_404, render, redirect
from datetime import datetime
from django.http import HttpResponse
from apps.catalogue.models import Product, Review
from apps.catalogue.forms import ProductForm, ReviewForm

def catalogue_view(request):
    products = Product.objects.all()
    query = request.GET.get('q')
    category_filter = request.GET.get('category')

    if query:
        products = products.filter(name__icontains=query)
    
    if category_filter:
        products = products.filter(category=category_filter)

    return render(request, 'catalogue.html', {
        'products': products,
        'categories': Product.CATEGORY_CHOICES 
    })


def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('show_product')  # Redirect after saving
    else:
        form = ProductForm()

    return render(request, 'create_product.html', {'form': form})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product).order_by('-created_at')  # Fetch all reviews for this product
    
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

    return render(request, 'details.html', {'product': product, 'reviews': reviews, 'form': form})

