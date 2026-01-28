from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.contrib.auth.decorators import login_required
from .forms import ProductCreateForm
from django.urls import reverse


@login_required
def product_list(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    return render(request, 'main/product/list.html', 
                  {'category': category,
                   'categories': categories,
                   'products': products})

@login_required
def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    related_products = Product.objects.filter(category=product.category,
                                              available=True).exclude(id=product.id)[:4]
    cart_product_form = CartAddProductForm()

    return render(request, 'main/product/detail.html', {'product': product,
                                                        'related_products': related_products,
                                                        'cart_product_form': cart_product_form})


@login_required
def add_product(request):
    # Allow any authenticated user to create a product; category choices are limited to existing categories
    if request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False, seller=request.user)
            product.seller = request.user
            product.save()
            return redirect(reverse('main:product_details', args=[product.id, product.slug]))
    else:
        form = ProductCreateForm()

    return render(request, 'main/product/add.html', {'form': form})