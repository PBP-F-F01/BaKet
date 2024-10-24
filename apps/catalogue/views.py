from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from apps.catalogue.models import Product, Review
from apps.catalogue.forms import ProductForm, ReviewForm
from django.contrib.auth.decorators import login_required

from .models import *

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

# @login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user, defaults={'user': request.user})

    # Check if the product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    # Increase quantity if it already exists
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    # Return JSON response if it's an AJAX request
    if request.is_ajax():
        cart_count = cart.cartitem_set.count()
        return JsonResponse({'cart_count': cart_count})

    return redirect('view_cart')

# @login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    total = cart.get_total_price()
    cart_count = cart.cartitem_set.count()

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'cart_count': cart_count
    })

# @login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('view_cart')

# @login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    if request.method == "POST":
        # Create an order
        order = Order.objects.create(user=request.user, cart=cart)
        return redirect('order_confirmation', order_id=order.id)

    total = cart.get_total_price()
    return render(request, 'cart/checkout.html', {
        'total': total,
        'cart': cart
    })

# @login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'cart/order_confirmation.html', {'order': order})
