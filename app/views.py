from .models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from .forms import *
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
import razorpay
from django.conf import settings
from django.utils import timezone
# Create your views here.




def home(request, city_name=None):
    cities = CityRegister.objects.all()
    product = Product.objects.all()
    category_objects = category.objects.all()
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    wishitem = 0
    if request.user.is_authenticated:
        wishitem = len(Wishlist.objects.filter(user=request.user))
        
    cart_product_ids = []
    if request.user.is_authenticated:
        cart_product_ids = Cart.objects.filter(user=request.user).values_list('product__id', flat=True)

    context = {
        'city': cities,
        'category_objects':category_objects,
        'product': product,
        'totalitem': totalitem,
        'wishitem': wishitem,
        'cart_product_ids': cart_product_ids, 
    }
    return render(request, 'app/index.html', context)

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def all_product(request):
    cities = CityRegister.objects.all()
    all_products = Product.objects.all()
    category_objects = category.objects.all()
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    wishitem = 0
    if request.user.is_authenticated:
        wishitem = len(Wishlist.objects.filter(user=request.user))
        
    cart_product_ids = []
    if request.user.is_authenticated:
        cart_product_ids = Cart.objects.filter(user=request.user).values_list('product__id', flat=True)
    
    # Process the form data
    selected_sort = request.GET.get('sort', 'price_low_to_high')
    selected_price_range = request.GET.get('price_range', '1_100000')
    selected_city = request.GET.get('city', None)
    
    if selected_sort == 'price_low_to_high':
        all_products = all_products.order_by('after_discount')
    elif selected_sort == 'price_high_to_low':
        all_products = all_products.order_by('-after_discount')
    
    price_range_values = selected_price_range.split('_')
    min_price = int(price_range_values[0])
    max_price = int(price_range_values[1])
    all_products = all_products.filter(after_discount__gte=min_price, after_discount__lte=max_price)
    
    if selected_city:
        selected_city_obj = get_object_or_404(CityRegister, city=selected_city)
        all_products = all_products.filter(city=selected_city_obj)

    # Paginate the products
    page = request.GET.get('page', 1)
    paginator = Paginator(all_products, 12)  # Change 12 to the number of products you want per page
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    context = {
        'city': cities,
        'product': products,
        'category_objects': category_objects,
        'totalitem': totalitem,
        'wishitem': wishitem,
        'cart_product_ids': cart_product_ids,
        'selected_sort': selected_sort,
        'selected_price_range': selected_price_range,
        'selected_city': selected_city,
    }
    return render(request, 'app/all_product.html', context)


def all_category(request):
    cities = CityRegister.objects.all()
    products = Product.objects.all()
    ategory_objects = category.objects.all()
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    wishitem = 0
    if request.user.is_authenticated:
        wishitem = len(Wishlist.objects.filter(user=request.user))
        
    cart_product_ids = []
    if request.user.is_authenticated:
        cart_product_ids = Cart.objects.filter(user=request.user).values_list('product__id', flat=True)
    
    # Process the form data
    category_objects = category.objects.all()
    # ... (rest of the code)

    context = {
        'city': cities,
        'product': products,
        'category_objects':category_objects,
        'totalitem': totalitem,
        'wishitem': wishitem,
        'cart_product_ids': cart_product_ids,
       'category_objects':category_objects,
    }
    return render(request, 'app/all_category.html', context)



from django.db.models import F

def all_category_filter(request, category_id):
    # Get the selected category
    try:
        desired_category = category.objects.get(id=category_id)
    except category.DoesNotExist:
        desired_category = None

    # Filter products by category if a category is selected
    if desired_category:
        products = Product.objects.filter(category=desired_category)
    else:
        products = Product.objects.all()

    # Sort the products based on the selected sorting option
    sort_option = request.GET.get('sort', 'all_item')

    if sort_option == 'price_low_to_high':
        products = products.order_by('price')
    elif sort_option == 'price_high_to_low':
        products = products.order_by(F('price').desc())

    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    wishitem = 0
    if request.user.is_authenticated:
        wishitem = len(Wishlist.objects.filter(user=request.user))
        
    cart_product_ids = []
    if request.user.is_authenticated:
        cart_product_ids = Cart.objects.filter(user=request.user).values_list('product__id', flat=True)
    
    # Retrieve all categories for the filter dropdown
    category_objects = category.objects.all()
    

    context = {
        'product': products,
        'totalitem': totalitem,
        'wishitem': wishitem,
        'cart_product_ids': cart_product_ids,
        'category_objects': category_objects,
        'desired_category': desired_category, 
    }
    return render(request, 'app/all_category_filter.html', context)



@login_required
def remove_from_cart(request):
    if request.method == 'POST':
        prod_id = request.POST.get('prod_id')
        if prod_id:
            if request.user.is_authenticated:
                cart_item = Cart.objects.filter(user=request.user, product__id=prod_id).first()
                if cart_item:
                    cart_item.delete()
    return redirect('/')


from django.shortcuts import render
from .models import Product, CityRegister, Cart, Wishlist

def product(request, city_name=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    wishitem = 0
    if request.user.is_authenticated:
        wishitem = len(Wishlist.objects.filter(user=request.user))

    cart_product_ids = []
    if request.user.is_authenticated:
        cart_product_ids = Cart.objects.filter(user=request.user).values_list('product__id', flat=True)

    cities = CityRegister.objects.all()
    products = Product.objects.filter(city__city=city_name) if city_name else Product.objects.all()

    # Get the selected sorting option from the query parameter
    selected_sort = request.GET.get('sort', 'all_item')  # Default value is 'price_low_to_high'

    if selected_sort == 'price_low_to_high':
        products = products.order_by('after_discount')
    elif selected_sort == 'price_high_to_low':
        products = products.order_by('-after_discount')

    # Get the selected price range option from the query parameter
    selected_price_range = request.GET.get('price_range', '1_100000')  # Default value is '100_250'
    price_range_values = selected_price_range.split('_')
    min_price = int(price_range_values[0])
    max_price = int(price_range_values[1])
    products = products.filter(after_discount__gte=min_price, after_discount__lte=max_price)
    category_objects = category.objects.all()
    context = {
        'city': cities,
        'product': products,
        'totalitem': totalitem,
        'wishitem': wishitem,
        'cart_product_ids': cart_product_ids,
        'selected_sort': selected_sort,
        'selected_price_range': selected_price_range,
        'category_objects':category_objects,
    }
    return render(request, 'app/product.html', context)



@login_required
def product_details(request, id, city_name=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    wishitem = 0
    if request.user.is_authenticated:
        wishitem = len(Wishlist.objects.filter(user=request.user))
        
    cities = CityRegister.objects.all()
    related_product = Product.objects.filter(city__city=city_name) if city_name else Product.objects.all()
    product = get_object_or_404(Product, id=id)
    wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
    products = Product.objects.filter(city__city=city_name) if city_name else Product.objects.all()
    
    # Filter ProductsImage objects based on the current product
    product_images = ProductsImage.objects.filter(product=product)
    
    is_product_in_cart = Cart.objects.filter(user=request.user, product=product).exists()
    category_objects = category.objects.all()
    context = {
        'category_objects':category_objects,
        'city': cities,
        'product': product,
        'related_product': related_product,
        'totalitem': totalitem,
        'wishlist': wishlist,
        'wishitem': wishitem,
        'products': products,
        'product_images': product_images,  # Pass the filtered images
        'is_product_in_cart': is_product_in_cart,
    }
    return render(request, 'app/product_details.html', context)


def about(request):
    category_objects = category.objects.all()
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    wishitem=0
    if request.user.is_authenticated:
        wishitem=len(Wishlist.objects.filter(user=request.user))
    cities = CityRegister.objects.all()
    context = {
        'city': cities,
        'totalitem':totalitem,
        'wishitem':wishitem
    }
    return render(request, 'app/about.html', context)

def contact(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    
    wishitem = 0
    if request.user.is_authenticated:
        wishitem = len(Wishlist.objects.filter(user=request.user))
    
    cities = CityRegister.objects.all()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            message = form.cleaned_data['message']
            
            contact_message = ContactMessage(name=name, email=email, phone_number=phone_number, message=message)
            contact_message.save()

            messages.success(request, 'Your message was successfully sent We will contact you soon.')

            return redirect('/')
    else:
        form = ContactForm()

    context = {
        'city': cities,
        'totalitem': totalitem,
        'wishitem': wishitem,
        'form': form,
    }
    return render(request, 'app/contact.html', context)


class CustomerRegistrationView(View):
    def get(self, request):
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=0
        if request.user.is_authenticated:
            wishitem=len(Wishlist.objects.filter(user=request.user))
        form=CustomerRegistrationForm()
        return render(request, 'app/CustomerRegistration.html', locals())
    
    def post(self, request):
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=0
        if request.user.is_authenticated:
            wishitem=len(Wishlist.objects.filter(user=request.user))
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User Register Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'app/CustomerRegistration.html', locals())


class ProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=0
        if request.user.is_authenticated:
            wishitem=len(Wishlist.objects.filter(user=request.user))
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form})
    
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=0
        if request.user.is_authenticated:
            wishitem=len(Wishlist.objects.filter(user=request.user))
        if form.is_valid():
            
            customer = form.save(commit=False)
            customer.user = request.user  
            
            customer.save()
            
            messages.success(request, 'Profile updated successfully.')
            return redirect('address')
        
        messages.error(request, 'There was an error in the form submission.')
        return render(request, 'app/profile.html', {'form': form})

@login_required
def address_view(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    wishitem=0
    if request.user.is_authenticated:
        wishitem=len(Wishlist.objects.filter(user=request.user))
    addresses = Customer.objects.filter(user=request.user)
    context={
        'addresses': addresses,
        'totalitem':totalitem,
        'wishitem':wishitem
    }
    return render(request, 'app/address.html', context)

class updateAddress(View):
    def get(self, request, pk):
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=0
        if request.user.is_authenticated:
            wishitem=len(Wishlist.objects.filter(user=request.user))
        addresses = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=addresses)
        context={
            'addresses':addresses,
            'form':form,
            'totalitem':totalitem,
            'wishitem':wishitem
        }
        return render(request, 'app/update_address.html',context)
    def post(self, request, pk):
        customer = Customer.objects.get(pk=pk) 
        form = CustomerProfileForm(request.POST, instance=customer)  
    
        if form.is_valid():
            form.save()  

            messages.success(request, 'Updated successfully.')
            return redirect('address')

        messages.error(request, 'There was an error in the form submission.')
        return render(request, 'app/update_address.html', {'form': form})
@login_required
def delete_address(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    messages.success(request, 'Address deleted successfully.')
    return redirect('address')
@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect("/cart")
@login_required
def show_cart(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    wishitem=0
    if request.user.is_authenticated:
        wishitem=len(Wishlist.objects.filter(user=request.user))
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value=p.total_cost
        amount=amount + value
    totalamount=amount + 0
    return render(request, 'app/addtocart.html', locals())
@login_required
def show_wishlist(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    wishitem=0
    if request.user.is_authenticated:
        wishitem=len(Wishlist.objects.filter(user=request.user))
    user=request.user
    cart=Wishlist.objects.filter(user=user)
    amount=0
    for p in cart:
        value=p.total_cost
        amount=amount + value
    totalamount=amount + 0
    return render(request, 'app/wishlist.html', locals())


@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()  
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.total_cost
            amount += value
        totalamount = amount + 0
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount,
            
        }
        return JsonResponse(data)

@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        
        if c.quantity > 1:
            c.quantity -= 1
            c.save()
        
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.total_cost
            amount += value
        totalamount = amount + 0
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)
    
@login_required   
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.total_cost
            amount += value
        totalamount = amount + 0
        data = {
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)
    
@login_required   
def plus_wishlist(request):
    if request.method == "GET":
        prod_id=request.GET['prod_id']
        product=Product.objects.get(id=prod_id)
        user=request.user
        Wishlist(user=user, product=product).save()
        data={
            'message':"Wishlist Added Successfully",
        }
        return JsonResponse(data)
    
from django.http import JsonResponse
@login_required
def minus_wishlist(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user, product=product).delete()
        data = {
            'message': "Wishlist Remove Successfully",
        }
        return JsonResponse(data)

class checkout(View):
    def get(self, request):
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=0
        if request.user.is_authenticated:
            wishitem=len(Wishlist.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart = Cart.objects.filter(user=user)
        famount = 0
        for p in cart:
            value = p.total_cost
            famount += value
        totalamount = famount + 0
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRECT))
        data = {'amount': razoramount, "currency": "INR", "receipt": "order_rcptid_11"}
        payment_response = client.order.create(data=data)
        print(payment_response)
        # {'id': 'order_MGNG4yAXiprRoH', 'entity': 'order', 'amount': 16400, 'amount_paid': 0, 'amount_due': 16400, 'currency': 'INR', 'receipt': 'order_rcptid_11', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1689925656}
        order_id=payment_response['id']
        order_status=payment_response['status']
        if order_status == 'created':
            payment=Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status
                
            )
            payment.save()
        return render(request, 'app/checkout.html', locals())


class CODCheckout(View):
    def get(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user)
        totalamount = 0
        for p in cart:
            totalamount += p.total_cost
        totalamount += 0

        add = Customer.objects.filter(user=user)

        return render(request, 'app/checkout.html', {'cart': cart, 'add': add, 'totalamount': totalamount})

    def post(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user)
        totalamount = 0
        for p in cart:
            totalamount += p.total_cost
        totalamount += 0

        add = Customer.objects.filter(user=user)

        if cart.exists():
            cart_item = cart.first()
            product = cart_item.product
            ordered_quantity = cart_item.quantity  # Get the ordered quantity from the cart item
            
            try:
                your_order_instance = OrderPlaced.objects.filter(user=request.user).latest('order_date')
            except OrderPlaced.DoesNotExist:
                your_order_instance = None

            if your_order_instance:
                your_product_instance = product
                your_customer_instance = your_order_instance.customer
                order = OrderPlacedCOD(
                    user=user,
                    order=your_order_instance,
                    product=your_product_instance,
                    quantity=ordered_quantity,  # Save the ordered quantity here
                    customer=your_customer_instance,
                    order_date=timezone.now(),
                    status='Pending', 
                    total_amount=totalamount,
                )
                order.save()

                messages.success(request, 'COD order placed successfully.')

                cart.delete()

        
        return redirect('orderscod')



def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')

    user = request.user

    
    if not user.is_authenticated:
        return redirect('login')  

    try:
        customer = Customer.objects.get(id=cust_id)
        payment = Payment.objects.get(razorpay_order_id=order_id)
        if not payment.paid:
            payment.paid = True
            payment.razorpay_payment_id = payment_id
            payment.save()

            
            cart = Cart.objects.filter(user=user)
            for c in cart:
                OrderPlaced.objects.create(user=user, customer=customer, product=c.product, quantity=c.quantity, payment=payment)
                c.delete()

        return redirect("orders")

    except Customer.DoesNotExist:
        
        return redirect("error_page")  

    except Payment.DoesNotExist:
        
        return redirect("error_page")  

@login_required
def orders(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    wishitem=0
    if request.user.is_authenticated:
        wishitem=len(Wishlist.objects.filter(user=request.user))
    order_placed=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', locals())




@login_required
def orderscod(request):
    totalitem = len(Cart.objects.filter(user=request.user)) if request.user.is_authenticated else 0
    wishitem = len(Wishlist.objects.filter(user=request.user)) if request.user.is_authenticated else 0

    
    customer = request.user.customer if hasattr(request.user, 'customer') else None
    print("Customer:", customer)  

    
    order_placed = OrderPlacedCOD.objects.filter(user=request.user)
    print("Orders:", order_placed) 
    return render(request, 'app/orderscod.html', {'order_placed': order_placed, 'totalitem': totalitem, 'wishitem': wishitem})




def search_results(request):
    cities = CityRegister.objects.all()
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    wishitem=0
    if request.user.is_authenticated:
        wishitem=len(Wishlist.objects.filter(user=request.user))
    search_query = request.GET.get('q')
    if search_query:
    
        products = Product.objects.filter(
            Q(name__icontains=search_query) |
            Q(city__city__icontains=search_query) |
            Q(price__icontains=search_query) |
            Q(after_discount__icontains=search_query) |
           
            Q(long_dec__icontains=search_query) |
            Q(weight__icontains=search_query) 
            
        )
    else:
        products = Product.objects.all()
    
    context = {
        'products': products, 
        'search_query': search_query,
        'totalitem':totalitem,
        'wishitem':wishitem,
        'city': cities,
        
        }
    return render(request, 'app/search_results.html', context)

@login_required
def faq(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    wishitem=0
    if request.user.is_authenticated:
        wishitem=len(Wishlist.objects.filter(user=request.user))
    addresses = Customer.objects.filter(user=request.user)
    context={
        'addresses': addresses,
        'totalitem':totalitem,
        'wishitem':wishitem
    }
    return render(request, 'app/faq.html', context)


@login_required
def terms_condition(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    wishitem=0
    if request.user.is_authenticated:
        wishitem=len(Wishlist.objects.filter(user=request.user))
    addresses = Customer.objects.filter(user=request.user)
    context={
        'addresses': addresses,
        'totalitem':totalitem,
        'wishitem':wishitem
    }
    return render(request, 'app/terms_condition.html', context)



@login_required
def privacy(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    wishitem=0
    if request.user.is_authenticated:
        wishitem=len(Wishlist.objects.filter(user=request.user))
    addresses = Customer.objects.filter(user=request.user)
    context={
        'addresses': addresses,
        'totalitem':totalitem,
        'wishitem':wishitem
    }
    return render(request, 'app/privacy.html', context)



@login_required
def support_policy(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    wishitem=0
    if request.user.is_authenticated:
        wishitem=len(Wishlist.objects.filter(user=request.user))
    addresses = Customer.objects.filter(user=request.user)
    context={
        'addresses': addresses,
        'totalitem':totalitem,
        'wishitem':wishitem
    }
    return render(request, 'app/support_policy.html', context)




    