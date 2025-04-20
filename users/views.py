from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from . import forms,models
import requests

# Create your views here.


class Login(View):
    def get(self,req):
        if req.user.is_authenticated:
            res=requests.get("https://api.escuelajs.co/api/v1/products").json()

            products={}

            for product in res:
                products[product['category']['name']]=products.get(product['category']['name'],[])+[product]

            return render(req,'home.html',{'products':products,'prod_keys':dict.keys(products)})
        else:
            return render(req,'login.html')
    def post(self,req):
        if req.user.is_authenticated:
            return redirect('/')
    
        email=req.POST['email']
        password=req.POST['password']
        userdata=models.User.objects.filter(email=email)
        if len(userdata):
            user=authenticate(req,username=userdata[0].username,password=password)
            
            if user: 
                login(req,user)
                return JsonResponse({'err':False,'redirect':"/"})
            else : return JsonResponse({'err':True,'msg':['Incorrect credentials']})

        else : return JsonResponse({'err':True,'msg':['No user found']})

        
class Signup(View):
    def get(self,req):
        if req.user.is_authenticated:
            return redirect('/')
        else:
            return render(req,'signup.html')
    def post(self,req):
        if req.user.is_authenticated:
            return redirect('/')

        form=forms.SignupForm(req.POST)

        if form.is_valid():
                models.User.objects.create_user(username=req.POST['username'],email=req.POST['email'],password=req.POST['password'])
                user=authenticate(req,username=req.POST['username'],password=req.POST['password'])
                if user is not None:
                    login(req,user)
                    return JsonResponse({'err':False,'redirect':"/"})
                return JsonResponse({'err':True,'msg':['Something went wrong']})
        else :
            
            return JsonResponse({'err':True,'msg':["".join(i) for i in dict.values(form.errors)]})
        

@login_required(login_url='/')
def product_data(req):
    try:
        res=requests.get(f"https://api.escuelajs.co/api/v1/products/{req.GET['id']}").json()
        cart=models.Cart.objects.filter(user=req.user).first()
        already_in_cart=False
        if cart is not None:
            if models.CartItem.objects.filter(cart=cart,product=int(req.GET.get('id',0))).exists():
                already_in_cart=True
            
        return render(req,'product.html',{'product':res,'cart_sts':already_in_cart})
    except:
        return HttpResponse('something went wrong in our end<br>Please try again')
    

@login_required(login_url='/')
def add_to_cart(req):
    try:
        if req.POST.get('id') is None:
            return JsonResponse({'err':True,'msg':'Please provide the product id'})
        user=req.user

        cart,created=models.Cart.objects.get_or_create(user=user)

        item,item_created=models.CartItem.objects.get_or_create(cart=cart, product=req.POST['id'])

        item.save()

        return JsonResponse({'err':False})
    except:
        return JsonResponse({'err':True,'msg':'something went wrong in our end<br>Please try again'})
    
@login_required(login_url='/')
def remove_from_cart(req):
    try:
        if req.POST.get('id') is None:
            raise ValueError()
        cart=models.Cart.objects.filter(user=req.user).first()
        if cart is None:
            raise ValueError()
        models.CartItem.objects.filter(cart=cart,product=req.POST['id']).delete()
        return JsonResponse({'err':False})

    except:
        return JsonResponse({'err':True,'msg':'Something went wrong'})
    

@login_required(login_url='/')
def cart(req):
	try:
		cart=models.Cart.objects.filter(user=req.user).first()
		if cart is None:
			cart_items=[]
		else:
			cart_items=cart.item.all()
		
		cart_items_data=[]
		
		for cart_item in cart_items:
			cart_items_data.append(requests.get(f"https://api.escuelajs.co/api/v1/products/{cart_item.product}").json())
		return render(req,'cart.html',{'cart':cart_items_data})
	except :
		return HttpResponse("Something went wrong in our end<br>Please try again")
   # if cart is None:
			# cart_item=[]
   # else:
			# cart_item=cart.item
   # return render(req,'cart.html',{"cart":cart_item})
	# except:
 #   	return HttpResponse("Something went wrong in our end<br>Please try again")

def logout(res):
    if res.is_authenticated:
          logout()
    return redirect('/')