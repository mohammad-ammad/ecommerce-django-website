from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from .models.product import Product
from .models.categories import Category
from .models.customers import Customer
from .models.orders import Orders
from django.views import View
# Create your views here.
def index(request):
    if request.method == "GET":
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        category = Category.get_all_category()
        categoryid = request.GET.get('category')
        if categoryid:
            product = Product.get_all_products_by_categoryid(categoryid)
        else:
            product = Product.get_all_products()
        data = {}
        data['products'] = product
        data['category'] = category
        print("you are:", request.session.get('email'))
        return render(request, 'index.html', data)
    else:
        productcart = request.POST.get("productcart")
        remove = request.POST.get("remove")
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(productcart)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(productcart)
                    else:
                        cart[productcart] = quantity - 1
                else:
                    cart[productcart] = quantity + 1
            else:
                cart[productcart] = 1
        else:
            cart = {}
            cart[productcart] = 1
        request.session['cart'] = cart
        print(request.session['cart'])
        return redirect('homepage')

def signup(request):
    if request.method == "GET":
        return render(request, 'signup.html')
    else:
        postdata = request.POST
        firstname = postdata.get("firstname")
        lastname = postdata.get("lastname")
        email = postdata.get("email")
        phone = postdata.get("phone")
        password = postdata.get("password")
        customer = Customer(firstname=firstname, lastname=lastname, Email=email, phone=phone, password=password)
        # error handling
        value = {
            'firstname': firstname,
            'lastname': lastname,
            'email': email,
            'phone': phone
        }
        error_msg = None
        if not firstname:
            error_msg = "First name required"
        elif len(firstname) < 3:
            error_msg = "First name too small"
        if not lastname:
            error_msg = "last name required"
        elif len(lastname) < 3:
            error_msg = "last name too small"
        if not email:
            error_msg = "Email required"
        if not phone:
            error_msg = "Phone Number is required"
        elif len(phone) < 11:
            error_msg = "Phone Number must be 11 digit long"
        if not password:
            error_msg = "paswword required"
        elif len(password) < 6:
            error_msg = "Password must be 6 digit long"
        elif customer.isEmailExit():
            error_msg = "Email already exists!!"


        if not error_msg:
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('homepage')
        else:
            data = {
                'error_msg': error_msg,
                'value': value
            }
            return render(request, 'signup.html', data)

class Login(View):
    return_url = None
    def get(self, request):
            Login.return_url = request.GET.get('return_url')
            return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        error_msg = None
        customerEmail = Customer.get_customer_email(email)
        if customerEmail:
            ispassword = check_password(password, customerEmail.password)
            if ispassword:
                request.session['customer_id'] = customerEmail.id
                request.session['email'] = customerEmail.Email
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('homepage')
            else:
                error_msg = "Invaild password"
        else:
            error_msg = "Email doesn't exist!!"
        return render(request, 'login.html', {'error_msg': error_msg})


def products_details(request,pk):
    products = Product.objects.get(pk=pk)
    return render(request, 'products_details.html', {'product':products})

def logout(request):
    request.session.clear()
    return redirect('login')

def cart(request):
    ids = list(request.session.get('cart').keys())
    product = Product.get_product_by_id(ids)
    print(product)
    return render(request, 'cart.html', {'product':product})

def checkout(request):
    if request.method == "POST":
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        customerid = request.session.get('customer_id')
        cart = request.session.get('cart')
        products = Product.get_product_by_id(list(cart.keys()))
        for product in products:
            order = Orders(customer= Customer(customerid),
                           product=product,
                           price= product.price,
                           address=address,
                           phone=phone,
                           quantity=cart.get(str(product.id)))
            order.placeorder()
        request.session['cart'] = {}
        return redirect("cart")

def ordersView(request):
    if request.method == 'GET':
        customer = request.session.get('customer_id')
        order = Orders.get_orders_by_customerid(customer)
        return render(request, "orders.html", {'orders': order})