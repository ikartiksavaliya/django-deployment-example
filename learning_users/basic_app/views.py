from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'basic_app/index.html')

@login_required
def special(request):
    return HttpResponse('you are logged in')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    print("REGISTER VIEW CALLED")  # Add this line to check if function runs

    registered = False

    if request.method == 'POST':
        print("POST REQUEST RECEIVED")  # Debugging step

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            print("FORMS ARE VALID")  # Debugging step

            user = user_form.save()
            user.set_password(user.password)  # Hash password
            user.save()
            print("USER SAVED")

            profile = profile_form.save(commit=False)
            profile.user = user  # Link profile with user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            print("PROFILE SAVED")

            registered = True
        else:
            print("User Form Errors:", user_form.errors)
            print("Profile Form Errors:", profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/registration.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse ('account not active')
        else:
            print('someone tried to login and failed')
            print('username:{username} password {password}'.format(username,password))
            return HttpResponse('invalid login detailed supplied')

    else:
        return render(request,'basic_app/login.html',{})
