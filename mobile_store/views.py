from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from mobile_store.models import Category
from mobile_store.models import Page
from mobile_store.forms import CategoryForm
from mobile_store.forms import PageForm
from mobile_store.forms import ContactForm
from mobile_store.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from mobile_store.bing_search import run_query
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import get_template
from django.core.mail import send_mail
from mobile_store.models import Item
from mobile_store.models import Order
from mobile_store.models import OrderItem
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


class HomeView(ListView):
    model = Item
    paginate_by = 8
    template_name = 'mobile_store/index.html'


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context_dict = {
                'object':order
            }
            
            return render(self.request, 'mobile_store/order_summary.html', context=context_dict)
        except ObjectDoesNotExist:
            messages.error(self.request, "There is no active order")
            return redirect('/')
        
        
    

def product(request):
    context_dict = {
        'items': Item.objects.all()
    }
    return render(request, 'mobile_store/product.html', context=context_dict)

class ItemDetailView(DetailView):
    model = Item
    template_name = 'mobile_store/product.html'

@login_required
def add_to_basket(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item,created = OrderItem.objects.get_or_create(item=item
    , user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Quantity of this item has been added")
            return redirect('mobile_store:order_summary')
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to basket")
            
            return redirect('mobile_store:order_summary')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to basket")
        return redirect('mobile_store:order_summary')


@login_required
def remove_from_basket(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user, ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from basket")
            return redirect('mobile_store:order_summary')
        else:
        
            messages.info(request, "This item was not in basket")
            return redirect('mobile_store:product', slug=slug)
    else:
   
        messages.info(request, "No current order")
        return redirect('mobile_store:product', slug=slug)

@login_required
def remove_single_item_from_basket(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user, ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()

            else:
                order.items.remove(order_item)

            messages.info(request, "Quantity of this item has been decreased")
            return redirect('mobile_store:order_summary')
        else:
        
            messages.info(request, "This item was not in basket")
            return redirect('mobile_store:product', slug=slug)
    else:
   
        messages.info(request, "No current order")
        return redirect('mobile_store:product', slug=slug)

    


def checkout_page(request):
    return render(request, 'mobile_store/checkout_page.html')
    

    

def about(request):
    context_dict = {'boldmessage': 'This tutorial has been put together by Craig'}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    return render(request, 'mobile_store/about.html', context=context_dict)

def basket(request):
    return render(request, 'mobile_store/basket.html')

def reviews(request):
    return render(request, 'mobile_store/reviews.html')

def iphoneXR(request):
    return render(request, 'mobile_store/iphoneXR.html')

def contact_us(request):
    form = ContactForm        
    context_dict = {}


    form= ContactForm(request.POST or None)
    if form.is_valid():
        
        firstname = request.POST.get('firstname')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        feedback = request.POST.get('feedback')

       

        subject = "comment"
        comment= firstname + " with the email, " + email + ", sent the following message:\n\n" + feedback + ". We will get back to your message in due course.\n\n" + "Best wishes from the Mobile Store Team";
        send_mail(subject, comment, 'mobilestoregu@gmail.com', [email])


        context_dict['firstname'] = firstname
        context_dict['surname'] = surname
        context_dict['email'] = email
        context_dict['feedback'] = feedback
        
        return render(request, 'mobile_store/contacting_us.html', context=context_dict)

    else:
        context =  {'form': form}
        return render(request, 'mobile_store/contact_us.html', context) 
            
    



def apple(request):
    return render(request, 'mobile_store/apple.html')

def android(request):
    return render(request, 'mobile_store/android.html')

def contacting_us(request):
    firstname = request.POST.get('firstname')
    context= {'firstname':firstname}
    

    return render(request, 'mobile_store/contacting_us.html', context)




def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            context_dict['result_list'] = run_query(query)
            context_dict['query'] = query

    return render(request, 'mobile_store/category.html', context=context_dict)

@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('/mobile_store/')
        else:
            print(form.errors)
    return render(request, 'mobile_store/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect('/mobile_store/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('mobile_store:show_category',
                                        kwargs={'category_name_slug':category_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'mobile_store/add_page.html', context=context_dict)
        
#def register(request):
   # registered = False
   # if request.method == 'POST':
        #user_form = UserForm(request.POST)
       # profile_form = UserProfileForm(request.POST)

       # if user_form.is_valid() and profile_form.is_valid():
          #  user = user_form.save()
          #  user.set_password(user.password)
          #  user.save()

            #profile = profile_form.save(commit=False)
           # profile.user = user

           # if 'picture' in request.FILES:
             #   profile.picture = request.FILES['picture']

           # profile.save()
            #registered = True
      #  else:
           # print(user_form.errors, profile_form.errors)
  #  else:
        #user_form = UserForm()
        #profile_form = UserProfileForm()

   # return render(request,
                #  'rango/register.html',
                 # context = {'user_form': user_form,
                          #   'profile_form': profile_form,
                          #   'registered': registered})

#def user_login(request):
    #if request.method == 'POST':
      #  username = request.POST.get('username')
       # password = request.POST.get('password')

        #user = authenticate(username=username, password=password)

       # if user:
           # if user.is_active:
               # login(request, user)
               # return redirect(reverse('rango:index'))
           # else:
               # return HttpResponse("Your Rango account is disabled.")

     #   else:
           # print(f"Invalid login details: {username}, {password}")
           # return HttpResponse("Invalid login details supplied.")

   # else:
       # return render(request, 'rango/login.html')

@login_required
def restricted(request):
    return render(request, 'mobile_store/restricted.html')
    #return HttpResponse("Since you're logged in, you can see this text!")

#@login_required
#def user_logout(request):
    #logout(request)
    #return redirect(reverse('rango:index'))

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request,
                                               'last_visit',
                                               str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
        
    request.session['visits'] = visits

#def search(request):

    #result_list = []
  #  if request.method == 'POST':
    #    query = request.POST['query'].strip()
     #   if query:
     #       result_list = run_query(query)

   # return render(request, 'rango/search.html', {'result_list': result_list})


    
