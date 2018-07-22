from django.shortcuts import render
from basic_app.forms import UserForm
#
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def index(request):
    return render(request, 'basic_app/index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            return render(request,'basic_app/registration.html', 
                                {'user_form': user_form,
                                'registered':registered,})
    else:
        user_form = UserForm()
    
    return render(request,'basic_app/registration.html', 
                                {'user_form': user_form,
                                'registered':registered})

def user_login(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponseRedirect("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login and failed!")
            print("Usename: {} and password {}".format(username, password))
            return render(request, 'basic_app/login.html',{ 'error_message': 'Invalid login details supplied!'})
    else:
        return render(request, 'basic_app/login.html',{})