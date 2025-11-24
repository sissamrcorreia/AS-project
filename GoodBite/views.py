from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render
from allauth.mfa.adapter import get_adapter as get_mfa_adapter
from allauth.mfa.models import Authenticator

from GoodBite.signals import User
from .forms import ProductForm, UserUpdateForm, ProfileUpdateForm
from .models import Product, Profile
from django.contrib import messages
from django.db.models import Sum, Count, F, Q, DecimalField, ExpressionWrapper
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied

def home(request):
    return render(request, 'main/home.html')

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
                form.save()
                form_profile.save()
                messages.success(request, "Data saved successfully")
                return redirect('profile', username=user.username)
        else:
            if form.errors:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)
                edit_mode = True
            else:
                birthdate_errors = form_profile.errors.get('birthdate')
                phone_number_errors = form_profile.errors.get('phone_number')

                if birthdate_errors:
                    messages.error(request, birthdate_errors[0])

                if phone_number_errors:
                    messages.error(request, f"Phone Number Error: {phone_number_errors[0]}")

                if not birthdate_errors and not phone_number_errors:
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
    return redirect('account_signup')

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
        return render(request, '403.html', status=403)
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


@staff_member_required
def statistics(request):
    # Top sellers
    top_sellers = User.objects.annotate(
        total_products=Count('products'),
        total_units_sold=Sum(F('products__initial_stock') - F('products__stock')),
        total_revenue=Sum(
            ExpressionWrapper(
                (F('products__initial_stock') - F('products__stock')) * F('products__price'),
                output_field=DecimalField()
            )
        )
    ).filter(
        total_units_sold__gt=0
    ).order_by('-total_revenue')[:10]

    # Top products
    top_products = Product.objects.annotate(
        units_sold=ExpressionWrapper(
            F('initial_stock') - F('stock'),
            output_field=DecimalField()
        ),
        revenue=ExpressionWrapper(
            (F('initial_stock') - F('stock')) * F('price'),
            output_field=DecimalField()
        )
    ).filter(units_sold__gt=0).order_by('-units_sold')[:10]

    # Products with most stock
    products_most_stock = Product.objects.filter(stock__gt=0).order_by('-stock')[:10]

    # Products with low stock (less than 20% of initial)
    low_stock_products = Product.objects.annotate(
        stock_percentage=ExpressionWrapper(
            F('stock') * 100.0 / F('initial_stock'),
            output_field=DecimalField()
        )
    ).filter(
        initial_stock__gt=0,
        stock_percentage__lt=20,
        stock__gt=0
    ).order_by('stock_percentage')[:10]

    # Out of stock products
    out_of_stock = Product.objects.filter(stock=0, initial_stock__gt=0)[:10]

    # General statistics
    total_products = Product.objects.count()
    total_active_products = Product.objects.filter(stock__gt=0).count()
    
    total_units_sold_all = Product.objects.aggregate(
        total=Sum(F('initial_stock') - F('stock'))
    )['total'] or 0

    total_revenue_all = Product.objects.aggregate(
        total=Sum(
            ExpressionWrapper(
                (F('initial_stock') - F('stock')) * F('price'),
                output_field=DecimalField()
            )
        )
    )['total'] or 0

    total_stock_value = Product.objects.aggregate(
        total=Sum(
            ExpressionWrapper(
                F('stock') * F('price'),
                output_field=DecimalField()
            )
        )
    )['total'] or 0

    # Products by price range
    price_ranges = [
        {'label': '0-10€', 'count': Product.objects.filter(price__lt=10).count()},
        {'label': '10-50€', 'count': Product.objects.filter(price__gte=10, price__lt=50).count()},
        {'label': '50-100€', 'count': Product.objects.filter(price__gte=50, price__lt=100).count()},
        {'label': '100-500€', 'count': Product.objects.filter(price__gte=100, price__lt=500).count()},
        {'label': '500€+', 'count': Product.objects.filter(price__gte=500).count()},
    ]

    # Most expensive products
    most_expensive = Product.objects.order_by('-price')[:5]

    # Average price
    avg_price = Product.objects.aggregate(avg=Sum('price'))['avg'] or 0
    if total_products > 0:
        avg_price = avg_price / total_products

    context = {
        'top_sellers': top_sellers,
        'top_products': top_products,
        'products_most_stock': products_most_stock,
        'low_stock_products': low_stock_products,
        'out_of_stock': out_of_stock,
        'total_products': total_products,
        'total_active_products': total_active_products,
        'total_units_sold': total_units_sold_all,
        'total_revenue': total_revenue_all,
        'total_stock_value': total_stock_value,
        'price_ranges': price_ranges,
        'most_expensive': most_expensive,
        'avg_price': avg_price,
    }

    return render(request, 'main/statistics.html', context)

class UserDeleteView(DeleteView):
    """
    Deletes the current user's account and logs them out.
    """
    model = get_user_model()
    success_url = reverse_lazy('home')
    template_name = 'main/confirm_delete_profile.html'
    
    # 1. Ensure only the currently logged-in user can delete their profile
    def get_object(self, queryset=None):
        user_obj = get_object_or_404(self.model, username=self.kwargs['username'])
        
        # Security check: User can only delete their own profile, unless they are admin
        if self.request.user != user_obj and not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to delete this profile.")
            
        return user_obj

    # 2. Add an extra step to log the user out after deletion
    def form_valid(self, form):
        response = super().form_valid(form)
        logout(self.request)
        return response

    # 3. Apply the login_required decorator
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)