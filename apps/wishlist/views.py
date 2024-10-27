from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from apps.catalogue.models import Product
from apps.wishlist.models import Wishlist

# Create your views here.

@login_required
def wishlist_view(request):
    # wishlists = Wishlist.objects.filter(user=request.user)
    wishlist_items = Wishlist.objects.all().select_related('product')
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
