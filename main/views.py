from django.shortcuts import get_object_or_404, render, redirect
from datetime import datetime
from django.http import HttpResponse
from main.models import Product, Review
from main.forms import ProductForm, ReviewForm

def index(request):
    context = {
        'current_time': datetime.now(),
    }
    return render(request, "main.html", context)

def show_product(request):
    products = Product.objects.all()
    return render(request, "list_product.html", {'products': products})

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

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('show_product')  # Redirect after saving
    else:
        form = ProductForm()

    return render(request, 'create_product.html', {'form': form})