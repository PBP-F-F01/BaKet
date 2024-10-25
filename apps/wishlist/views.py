from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from apps.catalogue.models import Product
from apps.wishlist.models import Wishlist

# Create your views here.

def wishlist_view(request):
    # wishlists = Wishlist.objects.filter(user=request.user)
    wishlists = Wishlist.objects.all()
    query = request.GET.get('q')
    categories = request.GET.getlist('category')
    sort_option = request.GET.get('sort')

    # Handle search
    if query:
        wishlists = wishlists.filter(name__icontains=query)

    # Handle filtering by category
    if categories:
        wishlists = wishlists.filter(category__in=categories)

    # Handle sorting
    if sort_option == 'price_asc':
        wishlists = wishlists.order_by('price')
    elif sort_option == 'price_desc':
        wishlists = wishlists.order_by('-price')

    context = {
        'products': wishlists,
        'categories': Product.CATEGORY_CHOICES,
        'selected_categories': categories,  
        'selected_sort': sort_option,
    }

    return render(request, 'wishlist.html', context)

@login_required
def add_to_wishlist(request, product_id):
    # Get the product by its ID
    product = get_object_or_404(Product, id=product_id)
    
    # Check if the product is already in the wishlist
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    
    if created:
        # If the item was newly added, you can show a success message
        return JsonResponse({'message': 'Product added to wishlist.'}, status=201)
    else:
        # If the product is already in the wishlist, you can show a message
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
