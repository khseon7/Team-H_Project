from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import UserForm


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

def detail(request):
    hotplace=hotplace.objects.all()