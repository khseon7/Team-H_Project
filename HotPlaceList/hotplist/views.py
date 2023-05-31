from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from .models import HotPlaces,Review
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout



# Create your views here.
def index(request):
    return render(request, 'hotplist/index.html')    

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('index')
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
            return redirect('hotplist:detail')
        else:
            print("Not User")
            return redirect('hotplist:login')
        
    else:
        return render(request, 'hotplist/login.html')

@login_required
def detail(request):
    data=HotPlaces.object.all()
    