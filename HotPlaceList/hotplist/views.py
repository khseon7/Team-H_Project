from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Review, User, HotPlaces, SavedPlaces
from .forms import ReviewForm, UserForm, PlaceForm

def index(request):
    datas = HotPlaces.objects.all()
    return render(request, 'hotplist/index.html', {'list':datas})

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
            context = {'form': form}
            return render(request, 'hotplist/create.html',context)
    else:
        form = PlaceForm()
        return render(request, 'hotplist/create.html',{'form':form})

def details(request, HP_id):
    HP_data = get_object_or_404(HotPlaces, pk = HP_id)
    Review_data = Review.objects.filter(store = HP_data)
    if request.user.is_authenticated:
        SP_data = SavedPlaces.objects.filter(user = request.user).values_list('saved', flat=True) 
        print(SP_data)
        saved = False
        if HP_data.id in SP_data:
            saved = True
        return render (request, 'hotplist/detail.html', {'HP_data':HP_data, 'Review_data':Review_data, 'SP_data':SP_data, 'saved':saved})
    else:
        return render(request, 'hotplist/detail.html', {'HP_data':HP_data, 'Review_data':Review_data})

@login_required(login_url = 'hotplist:login')
def review_create(request,HP_id):
    a = get_object_or_404(HotPlaces, pk = HP_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            content = form.save(commit = False)
            content.pub_date = timezone.now()
            content.author = request.user
            content.store = a
            content.save()
            return redirect('hotplist:review_create', HP_id = a.id)
        else:
            return redirect('hotplist:review_create')
    else:
        form = ReviewForm()
        return render(request, 'hotplist/reviewCreate.html', {'form':form})

@login_required(login_url = "hotplist:login")
def review_delete(request, item_id):
    data = get_object_or_404(Review, pk = item_id)
    data.delete()
    return redirect('hotplist:details', HP_id = data.store.id)

@login_required(login_url = "hotplist:login")
def review_modify(request, item_id):
    data = get_object_or_404(Review, pk = item_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            modify = form.save(commit = False)
            modify.pub_date = timezone.now()
            modify.save()
            return redirect("hotplist:details", HP_id = data.store.id)
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
            raw_username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate( username = raw_username, password = raw_password)
            if user is not None:
                auth_login(request,user)
                return redirect("hotplist:index")
            else:
                return redirect("hotplist:signup")
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
        if user is not None:
            auth_login(request, user)
            return redirect("hotplist:index")
        else:
            return redirect('hotplist:login')
    else:
        return render(request, 'hotplist/login.html')           
    

def logout(request):
    auth_logout(request)
    return redirect("hotplist:index")



# - 로그인 - 진용
# - 맛집등록 - 주호(팀장)
# - 맛집 디테일(댓글,맛집정보,찜하기) - 학선
# - 댓글생성 (평점,작성자,시간 — 가시성(o),수정, 삭제는 작성자만) - 은혜
# - 프로필 정보(찜, 리뷰 리스트)- 선우