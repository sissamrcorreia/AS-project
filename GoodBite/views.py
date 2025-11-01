from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import logout, authenticate, login, get_user_model
from .forms import CustomUserCreationForm, ProductForm, UserUpdateForm, ProfileUpdateForm
from .models import Product, Profile
from django.contrib import messages
from django.db.models import Q

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

def profile(request, username):
    user_model = get_user_model()
    user = get_object_or_404(user_model, username=username)

    if request.user != user and not request.user.is_staff:
        return redirect('home')

    profile_obj, _ = Profile.objects.get_or_create(user=user)

    edit_mode = request.GET.get("edit") == "1"

    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)
        form_profile = ProfileUpdateForm(request.POST, request.FILES, instance=profile_obj)

        if form.is_valid() and form_profile.is_valid():
            try:
                form.save()
                form_profile.save()
                messages.success(request, "Data saved successfully")
                return redirect('profile', username=user.username)
            except Exception:
                messages.error(request, "Oh no, an unexpected error happened. Try again later.")
                edit_mode = True
        else:
            birthdate_errors = form_profile.errors.get('birthdate')
            if birthdate_errors:
                messages.error(request, birthdate_errors[0])
                edit_mode = True
            else:
                messages.error(request, "Oh no, an unexpected error happened. Try again later.")
                edit_mode = True
    else:
        form = UserUpdateForm(instance=user)
        form_profile = ProfileUpdateForm(instance=profile_obj)

    return render(request, 'main/profile.html', {
        'user_obj': user,
        'form': form,
        'form_profile': form_profile,
        "edit_mode": edit_mode
    })

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

@permission_required('GoodBite.can_edit_own_product', raise_exception=True)
@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.created_by != request.user:
        return render(request, '403.html', status=403)
    
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    
    return render(request, 'main/confirm_delete.html', {'product': product})

@login_required
def product_list(request):
    q = (request.GET.get('q') or '').strip()
    products = Product.objects.all().order_by('id')

    if q:
        products = products.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(created_by__username__icontains=q) |
            Q(created_by__first_name__icontains=q) |
            Q(created_by__last_name__icontains=q)
        )

    return render(request, 'main/products.html', {
        'products': products,
        'q': q,
    })

@login_required
def buy_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.stock <= 0:
        messages.error(request, f"Sorry, {product.name} is out of stock.")
        return redirect('product_list')

    product.stock -= 1
    product.save()

    messages.success(request, f"You successfully bought {product.name}! Stock left: {product.stock}")
    return redirect('product_list')