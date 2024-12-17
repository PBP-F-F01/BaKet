import json
from django.contrib import messages

from django.shortcuts import get_object_or_404, render, redirect
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from apps.catalogue.models import Product, Review, Cart, CartItem,  Order, LikeReview
from apps.catalogue.forms import ProductForm, ReviewForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.core import serializers
from django.db.models import Avg
from django.core.paginator import Paginator

from apps.wishlist.models import Wishlist

from .models import *

def is_staff_or_superuser(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

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

@login_required
@user_passes_test(is_staff_or_superuser)
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalogue:catalogue')  # Redirect after saving
    else:
        form = ProductForm()

    return render(request, 'add-product.html', {'form': form})

@csrf_exempt
# @login_required
# @user_passes_test(is_staff_or_superuser)
def add_product_api(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return JsonResponse({
                "id": str(product.id),
                "name": product.name,
                "price": product.price,
                "image": request.build_absolute_uri(product.image.url),
                "specs": product.specs,
                "category": product.category,
            }, status=201)
        else:
            return JsonResponse({"error": form.errors}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product).order_by('-created_at')  # Fetch all reviews for this product
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user  
            review.save()
            return redirect('catalogue:product_detail', product_id=product_id)  # Refresh the page after review submission
    else:
        form = ReviewForm()

    if request.user.is_authenticated:
        is_in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
        return render(request, 'details.html', {'product': product, 'form': form, 'reviews': reviews, 'is_in_wishlist': is_in_wishlist,})
    else:
        return render(request, 'details.html', {'product': product, 'form': form, 'reviews': reviews, 'is_in_wishlist': None,})
        
@csrf_exempt
@require_POST
@login_required
def add_review_ajax(request):
    prod_id =  request.POST.get('prod_id')
    product = Product.objects.get(id=prod_id)
    comment = strip_tags(request.POST.get('comment')) 
    rating = request.POST.get("rate")
    user = request.user

    # Ensure the rating is a valid number
    if not rating:
        messages.error(request, "Rating cannot be empty!")
        return JsonResponse({'status': 'error', 'message': "Rating cannot be empty!"}, status=400)

    
    if request.user.is_authenticated:

        # Check if the user has already reviewed this product
        existing_review = Review.objects.filter(user=user, product=product).first()
        if existing_review:
            existing_review.comment = comment
            existing_review.rating = rating
            existing_review.save()
            messages.success(request, "Review updated successfully.")

        else:
            Review.objects.create(user=user, product=product, comment=comment, rating=rating)
            
        return HttpResponse(b"CREATED", status=201)
    
    else:
        messages.error(request, "You need to log in to submit a review.")


@csrf_exempt
def delete_review(request, review_id):
    if request.method == "POST":
        review = Review.objects.get(pk=review_id)
        review.delete()
        return JsonResponse({"success": True, "message": "Review deleted successfully."})
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)


def show_review_json(request, product_id):
    reviews = Review.objects.filter(product__id=product_id)

    data = [
        {
            "id": review.id,
            "user": review.user.id,
            "is_user_review": request.user == review.user,
            "username": review.user.username,
            "product": str(review.product),
            "rating": review.rating,
            "comment": review.comment,
            "created_at": review.created_at.isoformat(),
            "likeReview_count": review.likeReview_count,
        }
        for review in reviews
    ]
    return JsonResponse(data, safe=False)


@login_required
@require_POST
@csrf_exempt
def like_review(request):
    review_id = request.POST.get('review_id')
    review = Review.objects.get(id=review_id)
    user = request.user

    # Check if the user has already liked the review
    like_review, created = LikeReview.objects.get_or_create(user=user, review=review)

    if created:
        # User liked the review
        review.likeReview_count += 1
        review.save()
        liked = True
    else:
        # User unliked the review
        like_review.delete()
        review.likeReview_count -= 1
        review.save()
        liked = False

    return JsonResponse({
        'liked': liked,
        'like_count': review.likeReview_count,
    })

@csrf_exempt
def create_review_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            product_id = data.get("product_id")
            if not product_id:
                return JsonResponse({"status": "error", "message": "Product ID is required"}, status=400)

            # Fetch the product object
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Product not found"}, status=404)

            # Create the review
            new_review = Review.objects.create(
                user=request.user,
                product=product,
                rating=data.get("rating", 0),
                comment=data.get("comment", ""),
            )

            return JsonResponse({"status": "success"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

@csrf_exempt
def has_reviewed(request):
    if request.method == 'GET':
        user = request.user
        product_id = request.GET.get("product_id")

        if not product_id:
            return JsonResponse({"status": "error", "message": "Product ID is required"}, status=400)

        # Check if the review exists
        has_review = Review.objects.filter(user=user, product_id=product_id).exists()

        return JsonResponse({"has_reviewed": has_review}, status=200)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


def show_json(request):
    prod_id = request.POST.get('prod_id')
    data = Review.objects.filter(product=prod_id).select_related('user') 
    reviews = []

    if not data:
        return JsonResponse({"message": "No reviews found for this product"}, status=404)

    # Filter reviews based on the selected rating if it exists
    selected_rating = request.POST.get('star_rating')
    if selected_rating and selected_rating.isdigit():  # Ensure it's a digit
        data = data.filter(rating=int(selected_rating))

    for review in data:
        reviews.append({
            "id": review.id,
            "fields": {
                "username": review.user.username, 
                "is_user_review": request.user == review.user,
                "rating": review.rating,
                "comment": review.comment,
                "created_at": review.created_at,
                "likeReview_count": review.likeReview_count,
            }
        })

    print(f"Found {len(data)} reviews")  

    return JsonResponse(reviews, safe=False)

@csrf_exempt
def calculate_ratings(request):
    if request.method == "POST":
        data = json.loads(request.body)
        prod_id = data.get('prod_id')
        print(f"Product ID received: {prod_id}")  # Debugging output

        reviews = Review.objects.filter(product=prod_id)

        total_rating = sum(review.rating for review in reviews)
        count = reviews.count()
        average_rating = total_rating / count if count > 0 else 0.0

        response_data = {
            "average_rating": average_rating,
            "review_count": count,
        }

        return JsonResponse(response_data)

def product_list(request):
    products = Product.objects.all()
    query = request.GET.get('q')
    categories = request.GET.get('category')  # Comma-separated categories
    sort_option = request.GET.get('sort')

    # Handle search
    if query:
        products = products.filter(name__icontains=query)

    # Handle filtering by category
    if categories:
        category_list = categories.split(',')
        products = products.filter(category__in=category_list)

    # Handle sorting
    if sort_option == 'price_asc':
        products = products.order_by('price')
    elif sort_option == 'price_desc':
        products = products.order_by('-price')

    # Serialize products
    product_list = [
        {
            "id": str(product.id),
            "name": product.name,
            "price": product.price,
            "image": request.build_absolute_uri(product.image.url),
            "specs": product.specs,
            "category": product.category,
        }
        for product in products
    ]

    return JsonResponse({"products": product_list}, safe=False)

@login_required
def add_to_cart(request, product_id):
    # Fetch the product with the given UUID
    product = get_object_or_404(Product, id=product_id)
    
    # Get or create the cart for the user
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Get or create a cart item for the product in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    # If the cart item already exists, increment the quantity
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    # Check if the request is an AJAX request by looking at the request headers
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart_count = cart.cartitem_set.count()
        return JsonResponse({'cart_count': cart_count})

    # For non-AJAX requests, redirect to the cart page
    return redirect('catalogue:view_cart')

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    total = cart.get_total_price()
    cart_count = cart_items.count()

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'cart_count': cart_count
    })

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('catalogue:view_cart')

@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    total = cart.get_total_price()

    if request.method == "POST":
        # Create an order
        order = Order.objects.create(user=request.user, cart=cart, total=total)
        cart.cartitem_set.all().delete()
        return redirect('catalogue:order_confirmation', order_id=order.id)

    return render(request, 'checkout.html', {
        'total': total,
        'cart': cart
    })

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_confirmation.html', {'order': order, 'total': order.total})

