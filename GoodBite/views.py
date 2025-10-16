from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import logout, authenticate, login
from .forms import CustomUserCreationForm
from .models import Product
from .forms import ProductForm

# Create your views here.
def home(request):
    return render(request, 'main/home.html')

@login_required
def features(request):
    return render(request, 'main/features.html')

@login_required
def products(request):
    products = Product.objects.all()
    return render(request, 'main/products.html', {'products': products})

def exit(request):
    logout(request)
    return redirect('home')

def register(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()

            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            login(request, user)

            return redirect('home')
        data['form'] = user_creation_form

    return render(request, 'registration/register.html', data)

# New views for RBAC
@permission_required('GoodBite.can_create_product', raise_exception=True)
@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'main/products.html', {'form': form, 'create_mode': True})

@permission_required('GoodBite.can_edit_own_product', raise_exception=True)
@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.created_by != request.user:
        return render(request, '403.html', status=403)  # TODO: Custom 403 page if not owner
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'main/products.html', {'form': form, 'edit_mode': True, 'product': product})

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'main/products.html', {'products': products})