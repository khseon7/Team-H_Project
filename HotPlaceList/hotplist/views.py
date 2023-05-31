from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from .models import HotPlaces,Review



# Create your views here.
def index(request):
    return render(request, 'hotplist/index.html')    

def signin(request):
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
    return render(request, 'hotplist/signin.html', {'form': form})

def signup(request):
    return render(request,'hotplist/detail.html')

@login_required
def detail(request):
    data=HotPlaces.object.all()
    