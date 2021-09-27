import uuid
import random #random and string is used to generate random numbers/alphabets
import string
import requests #request and json is used for data interchange,sending information to another app and getting another info back
import json

from django.contrib.auth.models import User


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

from .forms import SignupForm,UpdateForm
from .models import Product, Category, Profile, ShopCart, PaidOrder

# Create your views here.
def index(request):
    feautured = Product.objects.filter(featured=True)
    New_arrival = Product.objects.filter(new_arrival=True)

    context={
        'feautured':feautured,
        'New_arrival':New_arrival
    }

    return render(request, 'index.html', context)

def categories(request):
    categories = Category.objects.all() #querying all the categories in the db

    context = {
        'categories' : categories
    }
    return render(request, 'categories.html',context)

def all_products(request):
    goods = Product.objects.all() #querying all the products in the db

    context = {
        'goods' : goods
    }
    return render(request, 'all_products.html', context)

def prod_category(request, id):
    single = Product.objects.filter(category_id=id)

    context = {
        'single' : single,
    }
    return render(request, 'prod_category.html', context)        


def prod_detail(request,id):
    detail = Product.objects.get(pk=id)

    context = {
        'detail' : detail
    }
    return render(request, 'detail.html', context)  


#Authentication defined
def loginform(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('profile')
        else:
            messages.info(request, 'username/password invalid')
            return redirect('loginform')

    return render(request, 'login.html')  


def logoutform(request):
    logout(request)
    return redirect('loginform')  

def signupform(request):
    regform = SignupForm()
    if request.method == 'POST':
        regform = SignupForm(request.POST)
        if regform.is_valid(): #if django validates that this data can be stored in the db
            reg = regform.save()
            newreg = Profile(user=reg)  #
            newreg.save()
            login(request, reg)
            messages.success(request, 'your signup is successful')
            return redirect('loginform')
        else:
            messages.warning(request, regform.errors) 
            return redirect('signupform')  

    context = {
        'regform':regform
    }        
    return render(request, 'signup.html', context) 

 #authentication done
 #    
#profile
@login_required(login_url='loginform')
def profile(request):
    profile = Profile.objects.get(user__username= request.user.username)

    context = {
        'profile':profile
    }
    return render(request, 'profile.html', context)

   
@login_required(login_url='loginform')
def update(request):  #user profile update
    updateform = UpdateForm(instance=request.user.profile)
    if request.method == 'POST':
        updateform = UpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if updateform.is_valid():
            updateform.save()
            messages.success(request, 'profile update successful')
            return redirect('profile')
        

    context = {
        'updateform' : updateform
    } 

    return render(request, 'update.html', context) 
    #profile done                                
      
#password change
@login_required(login_url='loginform')
def password(request):
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password change successful')
            return redirect('profile')
        else:
            messages.error(request, form.errors) 
            return redirect('password') 

    context = {
        'form':form
    }  

    return render(request, 'password.html', context)   

#shopcart
@login_required(login_url='loginform')

def shopcart(request):
    if request.method == 'POST':
        quant = int(request.POST['quantity'])
        dpid = request.POST['pid'] #the id of the products selected is saved in dpid
        apid = Product.objects.get(pk=dpid) #gets the primary key of each of the product id (dpid) saves in all the product id(apid)
        cart = ShopCart.objects.filter(paid_order=False, user__username= request.user.username)
        if cart: #check if cart is been created
            product = ShopCart.objects.filter(user__username=request.user.username,product=apid.id).first()
            if product: #check if product is in the cart
                product.quantity += quant #if in the cart.....increment quantity'pkl
                product.save()
                messages.success(request, 'Product added to cart')
                return redirect('all_products')

            else: #add new item in the cart
                newitem = ShopCart()
                newitem.user = request.user
                newitem.product = apid
                newitem.quantity = quant
                newitem.cart_code = cart[0].cart_code #every new item picked should be attached to the cart_code generated for the cart
                newitem.paid_order = False
                newitem.save()
                messages.success(request, 'Product added to cart')
                
        else:
            order_number=str(uuid.uuid4())  #at this point an order number was created to label the new cart
            newcart =  ShopCart()
            newcart.user = request.user
            newcart.product = apid
            newcart.quantity = quant
            newcart.cart_code = order_number
            newcart.paid_order = False
            newcart.save() 

        messages.success(request, 'Product added to cart!')
    return redirect('all_products')
        
    # return render(request, 'shopcart.html')  

@login_required(login_url='loginform')    
def cart(request):
    cart = ShopCart.objects.filter(paid_order=False, user__username= request.user.username)

    total = 0
    vat = 0
    grand_total = 0

    for item in cart:
       total += item.product.price * item.quantity

    vat = 0.075 * total

    grand_total = total + vat

    context = {
        'cart': cart,
        'total': total,
        'vat': vat,
        'grand_total': grand_total
    }
    return render(request, 'cart.html', context)    

# increase quantity of items
@login_required(login_url='loginform') 
def increase(request):
    increase = request.POST['addup']
    itemid = request.POST['itemid']
    newquantity = ShopCart.objects.get(pk=itemid)
    newquantity.quantity = increase
    newquantity.save()
    messages.success(request, 'Item quantity is updated')
    return redirect('cart')

#remove item
@login_required(login_url='loginform') 
def remove(request):
    remove = request.POST['del'] #posting a delete with del as per name in input tag.assigning post request to variable remove
    ShopCart.objects.filter(pk=remove).delete()
    messages.success(request, 'Item successfuly deleted from your cart')
    return redirect('cart')

#checkout
@login_required(login_url='loginform') 
def checkout(request):
    cart = ShopCart.objects.filter(paid_order=False, user__username= request.user.username)
    profile = Profile.objects.get(user__username= request.user.username)

    total = 0
    vat = 0
    grand_total = 0

    for item in cart:
       total += item.product.price * item.quantity

    vat = 0.075 * total

    grand_total = total + vat

    context = {
        'cart': cart,
        'grand_total': grand_total,
        'profile' : profile,
        'cart_code': cart[0].cart_code
    }
    return render(request, 'checkout.html', context)

#integrating to paystack API
@login_required(login_url='loginform') 
def paidorder(request):
    if request.method =='POST': 
    #at this function we are collecting data to take to paystack at the point of intergation
        api_key = 'sk_test_19cf2a301b21b310fb7f6d8c7e5e4377ba77232d' #api key from paystack
        curl = 'https://api.paystack.co/transaction/initialize' #the number with which to reach paystack
        call_back_url ='http://3.140.192.45/completed' # a template to show completed if transaction is successful
        # call_back_url ='http://localhost:8000/completed' # a template to show completed if transaction is successful
        total = float(request.POST['gtotal']) * 100
        order_num = request.POST['order_no'] #the cart number being sent to paystack
        ref_num = ''.join(random.choices(string.digits + string.ascii_letters, k=8))# random generated number being sent to paystack
        user = User.objects.get(username= request.user.username)

        headers = {'Authorization': f'Bearer {api_key}'} # the authorization being sent to paystack which is the api key
        data = {'reference': ref_num, 'amount':total, 'order_number':order_num, 'callback_url':call_back_url, 'email':user.email}#all the data being sent to paystack
    #collection of data for paystack use ends here

        #call now being ititiated to paystack
        try:
            r=requests.post(curl, headers=headers, json=data) #we are posting the curl url,the headers and the json(representing data) to paystack.transaction succussful then else block initiated
        except Exception:
            messages.error(request, 'Network busy, refresh your page and try again. Thank you')
            #exception block will hold brief incase transaction got an error
        else:
            transback = json.loads(r.text)#at this point its clear transaction was succesful
            rd_url = transback ['data']['authorization_url']
            paid = PaidOrder()
            paid.user = user
            paid.total_paid = total
            paid.cart_code = order_num
            paid.transac_code = ref_num
            paid.paid_order = True
            paid.first_name = user.profile.first_name
            paid.last_name = user.profile.last_name
            paid.phone = user.profile.phone
            paid.address = user.profile.address
            paid.city = user.profile.city
            paid.state = user.profile.state
            paid.save()

            #once items are taken out, the basket should become empty. to ensure this query the shopcart
            basket = ShopCart.objects.filter(user__username= request.user.username)
            for item in basket:
                item.paid_order=True
                item.save()

                #once items are sold out, take inventory. To ensure this query the Product
                stock = Product.objects.get(pk=item.product.id)
                stock.max_quantity -= item.quantity
                stock.save()
    
            return redirect(rd_url)        
        return redirect('checkout')

@login_required(login_url='loginform') 
def completed(request):
    profile = Profile.objects.get(user__username= request.user.username)

    context = {
        'profile':profile
    }

    return render(request, 'completed.html',context)            



