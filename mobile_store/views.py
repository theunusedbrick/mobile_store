from django.shortcuts import render
from django.http import HttpResponse, Http404
from mobile_store.models import Category
from mobile_store.models import Page
from mobile_store.forms import CategoryForm
from mobile_store.forms import PageForm
from django.shortcuts import redirect
from django.urls import reverse
from mobile_store.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from mobile_store.bing_search import run_query


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]
    
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = pages_list
   
    #context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}
    
    visitor_cookie_handler(request)
    #context_dict['visits'] = request.session['visits']
    #response = render(request, 'rango/index.html', context=context_dict)
    #return response
    return render(request, 'mobile_store/index.html', context=context_dict)

def about(request):
    context_dict = {'boldmessage': 'This tutorial has been put together by Craig'}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    return render(request, 'mobile_store/about.html', context=context_dict)

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
    
    