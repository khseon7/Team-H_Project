from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from . import models
from .models import Review, User, HotPlaces
from .forms import ReviewForm, UserForm, PlaceForm
from django.http import JsonResponse


def index(request):
    placeList = HotPlaces.objects.all()
    return render(request, 'hotplist/index.html', {'placeList': placeList})

@login_required(login_url= 'hotplist:login')
def create(request):
    if request.method == 'POST':
        form = PlaceForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit = False)
            data.original_rating = data.rating
            form.save()
            return redirect('hotplist:index')
        else:
            #context = {'form': form}
            return render(request, 'hotplist/create.html', {'form':form})
    else:
        form = PlaceForm()
        return render(request, 'hotplist/create.html',{'form':form})
    
def like(request, HP_id):
    HP_data = get_object_or_404(HotPlaces, pk=HP_id)
    Review_data = Review.objects.filter(store = HP_data)
    user = request.user
    if user in HP_data.like_users.all():
        HP_data.like_users.remove(user)
        liked = False
    else:
        HP_data.like_users.add(user)
        liked = True
    return render(request, 'hotplist/detail.html', {'HP_data': HP_data,'Review_data':Review_data, 'liked': liked})
    
def detail(request, HP_id):
    HP_data = get_object_or_404(HotPlaces, pk = HP_id) #pk에 가져온 HP_id를 저장, 해당 pk의 HotPlaces객체의 존재 여부를 따짐
    Review_data = Review.objects.filter(store = HP_data) #HotPlaces객체 값을 store에 저장하고 해당 store의 Review객체를 필터링하여 Review_data에 저장
    if request.user.is_authenticated:
        return render (request, 'hotplist/detail.html', {'HP_data':HP_data, 'Review_data':Review_data })
    else:
        return render(request, 'hotplist/detail.html', {'HP_data':HP_data, 'Review_data':Review_data})

@login_required(login_url = 'hotplist:login')
def review_create(request, HP_id):
    a = get_object_or_404(HotPlaces, pk = HP_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            content = form.save(commit = False)
            content.pub_date = timezone.now()
            content.author = request.user
            content.store = a
            content.save()
            return redirect('hotplist:index')
        else:
            return render(request, 'hotplist/reviewCreate.html', {'form':form})
    else:
        form = ReviewForm()
        return render(request, 'hotplist/reviewCreate.html', {'form':form})

@login_required(login_url = "hotplist:login")
def review_delete(request, item_id):
    data = get_object_or_404(Review, pk = item_id)
    data.delete()
    return redirect('hotplist:detail', HP_id = data.store.id)

@login_required(login_url = "hotplist:login")
def review_modify(request, item_id):
    data = get_object_or_404(Review, pk = item_id)
    a = get_object_or_404(HotPlaces, pk = data.store.id)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=data)
        if form.is_valid():
            modify = form.save(commit = False)
            modify.author = request.user
            modify.pub_date = timezone.now()
            modify.store = a
            modify.save()
            return redirect("hotplist:detail", HP_id = data.store.id)
        else:
            return render(request, 'hotplist/reviewCreate.html', {'form':form})
    else:
        form = ReviewForm()
        return render(request, 'hotplist/reviewCreate.html', {'form':form})
    
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate( username=username, password = raw_password)
            auth_login(request, user)
            return redirect("hotplist:index")
        else:
            form = UserForm(request.POST)
            return render(request, 'hotplist/signup.html' ,{'form':form})
    else:
        form = UserForm()
        return render(request, 'hotplist/signup.html',{'form':form})
    
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        auth_login(request, user)
        return redirect("hotplist:index") #아이디, 비번이 맞지 않을 때
    else:
        return render(request, 'hotplist/login.html')      

def logout(request):
    auth_logout(request)
    return redirect("hotplist:index")

def profile(request):
    user = request.user
    liked_HP_data = HotPlaces.objects.filter(like_users=user)
    user_reviews = Review.objects.filter(author=user)
    return render(request, 'hotplist/profile.html', {'liked_HP_data': liked_HP_data, 'user_reviews':user_reviews})

# - 프로필 정보(찜, 리뷰 리스트)
# - 로그인은 선택적으로 하지만 로그인 안하면 내 프로필 확인 불가, 찜하기 불가하고 오직 게시물 보기만 가능하다.
# - 게시글 수정,삭제는 해당 게시글 작성한 유저만 가능하게 만들기