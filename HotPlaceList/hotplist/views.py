from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from .models import HotPlaces,Review,WantList
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

# Create your views here.
def index(request):
    data=HotPlaces.objects.all()
    return render(request, 'hotplist/index.html',{'list':data})

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=raw_password)  # 사용자 인증
            auth_login(request, user)  # 로그인
            return redirect('hotplist:index')
        
        else:
            return redirect('hotplist:signup')
    else:
        form = UserForm()
        return render(request, 'hotplist/signup.html', {'form': form})

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            auth_login(request, user)
            return redirect('hotplist:index')
        else:
            return redirect('hotplist:login')
        
    else:
        return render(request, 'hotplist/login.html')

def logout(request):
    auth_logout(request)
    return redirect('hotplist:index')

@login_required
def detail(request):
    data=HotPlaces.objects.all()
    return render(request,'hotplist/detail.html')