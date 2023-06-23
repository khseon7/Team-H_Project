from django.contrib.auth import authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserForm,ReviewForm
from .models import HotPlaces,Review,WantList
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.utils import timezone

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
            if user is not None:
                auth_login(request, user)  # 로그인
                return redirect('hotplist:index')
            else:
                return redirect('hotplist:signup')
        
        else:
            form = UserForm(request.POST)
            return render(request, 'hotplist/signup.html', {'form': form})
    else:
        form=UserForm()
        return render(request,'hotplist/signup.html',{'form':form})

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

def eval_rating(HP_data,Review_data):
    rating=HP_data.origin_rating
    for data in Review_data:
        rating+=data.rating
    HP_data.rating=rating/(len(Review_data)+1)
    
def detail(request,HP_id):
    HP_data=get_object_or_404(HotPlaces, pk=HP_id)
    Review_data=Review.objects.filter(place=HP_data)
    eval_rating(HP_data,Review_data)
    return render(request, 'hotplist/detail.html',{"HP_data":HP_data,"Review_data":Review_data})

@login_required(login_url='hotplist:login')
def new_review(request,HP_id):
    HP=get_object_or_404(HotPlaces,pk=HP_id)
    if request.method=="POST":
        form=ReviewForm(request.POST)
        if form.is_valid():
            review=form.save(commit=False)
            review.author=request.user
            review.place=HP
            review.date=timezone.now()
            review.save()
            return redirect('hotplist:detail',HP_id=HP.id)
        else:
            form=ReviewForm(HP_id)
            return render('hotplist/new_review.html',{'HP':HP,'form':form})
    else:
        form=ReviewForm()
        return render(request,'hotplist/new_review.html',{'HP':HP,'form':form})

def edit_review(request,Review_id):
    Review=get_object_or_404(Review,pk=Review_id)
    if request.method=='POST':
        form=ReviewForm(request.POST,instance=Review)
        if form.is_valid():
            edit=form.save(commit=False)
            edit.date=timezone.now()
            edit.save()
            return redirect("hotplist:detail",HP_id=Review.place.id)
        else:
            form=ReviewForm(instance=Review)
            return render(request,'hotplist/new_review.html',{'form':form})
    else:
        form=ReviewForm(instance=Review)
        return render(request,'hotplist/new_review.html',{'form':form})

def delete_review(request,Review_id):
    target=get_object_or_404(Review,pk=Review_id)
    target.delete()
    return redirect('hotplist:detail',HP_id=target.place.id)

def my_profile(request):
    review_data=Review.objects.filter(author=request.user)
    return render(request,'hotplist/my_profile.html',{'review_data':review_data})