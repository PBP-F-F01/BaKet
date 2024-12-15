from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
from apps.catalogue.models import Product
from apps.wishlist.models import Wishlist

# Create your views here.

@login_required
def wishlist_view(request):
    # wishlists = Wishlist.objects.filter(user=request.user)
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    query = request.GET.get('q')
    categories = request.GET.getlist('category')
    sort_option = request.GET.get('sort')

    # Handle search
    if query:
        wishlist_items = wishlist_items.filter(product__name__icontains=query)

    # Handle filtering by category
    if categories:
        wishlist_items = wishlist_items.filter(product__category__in=categories)

    # Handle sorting
    if sort_option == 'price_asc':
        wishlist_items = wishlist_items.order_by('product__price')
    elif sort_option == 'price_desc':
        wishlist_items = wishlist_items.order_by('-product__price')

    context = {
        # 'wishlist_items': wishlist_items,
        'wishlist_items': [item.product for item in wishlist_items],  # List of Product objects
        'categories': Product.CATEGORY_CHOICES,
        'selected_categories': categories,  
        'selected_sort': sort_option,
    }

    return render(request, 'wishlist.html', context)

@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    
    if created:
        message = 'Product added to wishlist.'
        status = 'added'
    else:
        wishlist_item.delete()
        message = 'Product removed from wishlist.'
        status = 'removed'
    
    return JsonResponse({'message': message, 'status': status})

@login_required
def add_to_wishlist(request, product_id):
    # Get the product by its ID
    product = get_object_or_404(Product, id=product_id)
    
    # Check if the product is already in the wishlist
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    
    if created:
        return JsonResponse({'message': 'Product added to wishlist.'}, status=201)
    else:
        return JsonResponse({'message': 'Product is already in wishlist.'}, status=200)

@login_required
def remove_from_wishlist(request, product_id):
    # Get the product by its ID
    product = get_object_or_404(Product, id=product_id)
    
    # Find the wishlist item and delete it
    wishlist = Wishlist.objects.filter(user=request.user, product=product).first()
    
    if wishlist:
        wishlist.delete()
        return JsonResponse({'message': 'Product removed from wishlist.'}, status=200)
    else:
        return JsonResponse({'message': 'Product not found in wishlist.'}, status=404)

@login_required
def is_in_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = Wishlist.objects.filter(user=request.user, product=product)
    
    # Return the result as a JSON response
    return JsonResponse({'is_in_wishlist': wishlist.exists()})

@require_POST
@csrf_exempt
@login_required
def toggle_wishlist_api(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
    
        product = get_object_or_404(Product, id=product_id)
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
        
        if created:
            message = 'Product added to wishlist.'
            status = 'added'
        else:
            wishlist_item.delete()
            message = 'Product removed from wishlist.'
            status = 'removed'
    
        return JsonResponse({'message': message, 'status': status}, status=200)
    return JsonResponse({'message': 'Invalid request', 'status': 'error'}, status=400)

@login_required
def show_json(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    query = request.GET.get('q')
    categories = request.GET.get('category')  # Comma-separated categories
    sort_option = request.GET.get('sort')

    # Handle search by Product name
    if query:
        wishlist_items = wishlist_items.filter(product__name__icontains=query)

    # Handle filtering by Product category
    if categories:
        category_list = categories.split(',')
        wishlist_items = wishlist_items.filter(product__category__in=category_list)

    # Handle sorting by Product price
    if sort_option == 'price_asc':
        wishlist_items = wishlist_items.order_by('product__price')
    elif sort_option == 'price_desc':
        wishlist_items = wishlist_items.order_by('-product__price')

    # Serialize products from Wishlist items
    product_list = [
        {
            "id": str(wishlist_item.product.id),
            "name": wishlist_item.product.name,
            "price": wishlist_item.product.price,
            "image": request.build_absolute_uri(wishlist_item.product.image.url),
            "specs": wishlist_item.product.specs,
            "category": wishlist_item.product.category,
            "added_on": wishlist_item.added_on,
        }
        for wishlist_item in wishlist_items
    ]

    return JsonResponse({"products": product_list}, safe=False)