from django.http import HttpResponse
from django.template import loader
from .models import Category, Product, Order, User
from .forms import LoginForm, SignUpForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
# Import models as needed inside the view functions
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

#-------Account
def sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            # Authenticate user using custom method (example assumes email-based authentication)
            user = User.objects.get(USERNAME_FIELD=username)
            authenticated_user = user.authenticate(username=username, password=password)
            if user is not None:
                # Log the user in
                login(request, user)
                # request.session['user_id'] = user.id
                # Redirect to dashboard or any other page
                return redirect('/')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'phone/login.html', {'form': form})


def sign_up(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
            user = authenticate(USERNAME_FIELD=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "phone/register.html", {"form": form, "msg": msg, "success": success})

def logout_view(request):
  """Logs out the user and redirects to login page."""
  # Logout the user using Django's logout function
  logout(request)
  # Optionally, clear any session data related to login
  # del request.session['user_data']  # Example removing user data
  return redirect('login')  # Redirect to login page after logout

#-------Cart
def view_cart(request):
    cart_items = Order.objects.filter(user=request.user)
    return render(request, 'phone/order.html', {'cart_items': cart_items})

@login_required
def add_to_cart(request, product_id):
    user_id = request.user.id  
    user = User.objects.get(id=user_id)
    product = Product.objects.get(id=product_id)
    cart_item, created = Order.objects.get_or_create(product=product, user=user)
    if created:
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1
    cart_item.save()
    return render(request, 'phone/order.html', {'user_id': user_id})

 
def remove_from_cart(request, item_id):
    cart_item = Order.objects.get(id=item_id)
    cart_item.delete()
    return redirect('order')

#-------Pages

def main(request):
  template = loader.get_template('phone/main.html')
  return HttpResponse(template.render())

def category_list(request):
  mycategorys = Category.objects.all().values()
  template = loader.get_template('phone/category_list.html')
  context = {'mycategory': mycategorys}
  return HttpResponse(template.render(context, request))

def product_detail(request, id):
  myproducts = Category.objects.get(pk=id)
  template = loader.get_template('phone/product_detail.html')
  context = {
    'myproduct': myproducts,
  }
  return HttpResponse(template.render(context, request))

def page_user(request):
  template = loader.get_template('phone/page_user.html')
  return HttpResponse(template.render())

def order_page(request):
  template = loader.get_template('phone/order.html')
  return HttpResponse(template.render())

# -----------search bar

def search_feature(request):
    if request.method == 'POST':
        search_query = request.POST['search_query']
        posts = Product.objects.filter(name=search_query)
        return render(request, 'phone/search_result.html', {'search_query':search_query, 'posts':posts})
    else:
        return render(request, 'phone/search_result.html',{})