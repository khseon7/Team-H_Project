from django.shortcuts import render,redirect,get_object_or_404
from .forms import HPForm,ReviewForm,UserForm
from django.contrib import messages
from .models import HotPlaces, Reviews, SavedPlaces
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.models import User




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


def profile(request, HP_author):
    if request.user != HP_author:
        SP_data = SavedPlaces.objects.filter(user = HP_author)
        Review_data = Reviews.objects.filter(author = HP_author)
        profile_name = get_object_or_404(User,pk = HP_author)
        return render(request, 'hotplist/profile.html', {'SP_data':SP_data, 'Review_data':Review_data, 'user':profile_name})
    else: 
        SP_data = SavedPlaces.objects.filter(user = request.user)
        Review_data = Reviews.objects.filter(author = request.user)
        profile_name = get_object_or_404(User,pk = HP_author)
        return render(request, 'hotplist/profile.html', {'SP_data':SP_data, 'Review_data':Review_data,'user':profile_name})


##첫 페이지, 맛집 리스트를 화면에 띄움
def index(request):
    # getting page value, with default of '1'
    page = request.GET.get("page",1)
    datas = HotPlaces.objects.order_by('-name')
    paginator = Paginator(datas, 10)
    page_obj = paginator.get_page(page)

    return render(request, 'hotplist/index.html', {'list':page_obj})

##평균평점 계산하는 function
def calculate_rating(HP_id):
    HP_data = get_object_or_404(HotPlaces, pk = HP_id)
    Review_data = Reviews.objects.filter(place = HP_data)
    count = 1
    sum = HP_data.original_rating
    print(sum)
    for items in Review_data.all():
        sum += items.rating
        count += 1
    avg_rating = sum/count
    print(avg_rating)
    return avg_rating

##평균평점을 데이터베이스에 업뎃하는 function
def update_rating(HP_id):
    HP_data = get_object_or_404(HotPlaces, pk = HP_id)
    HP_data.rating = calculate_rating(HP_id)
    HP_data.save()

@login_required(login_url= 'hotplist:login')
def create(request):
    if request.method == 'POST':
        form = HPForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit = False)
            data.original_rating = data.rating
            data.author = request.user
            form.save()
            return redirect('hotplist:index')
        else:
            context = {'form': form}
            return render(request, 'hotplist/create.html',context)
          
            # return HttpResponse("폼 인증 실패")
    else:
        form = HPForm()
        return render(request, 'hotplist/create.html',{'form':form})
    


def details(request, HP_id):
    HP_data = get_object_or_404(HotPlaces, pk = HP_id)
    Review_data = Reviews.objects.filter(place = HP_data)
    if request.user.is_authenticated:
        #returns queryset of values of single attribute('saved') in SavedPlaces table
        SP_data = SavedPlaces.objects.filter(user = request.user).values_list('saved', flat=True) 
        print(SP_data)
        saved = False
        if HP_data.id in SP_data:
            saved = True

        return render (request, 'hotplist/details.html', {'HP_data':HP_data, 'Review_data':Review_data, 'SP_data':SP_data, 'saved':saved})
    else:
        return render(request, 'hotplist/details.html', {'HP_data':HP_data, 'Review_data':Review_data})


def save(request, HP_id):
    HP_data = get_object_or_404(HotPlaces, pk = HP_id)
    JJim = SavedPlaces.objects.create(user = request.user, saved = HP_data)
    return redirect("hotplist:details", HP_id = HP_id)


def save_delete(request, HP_id):
    HP_data = get_object_or_404(HotPlaces, pk = HP_id )
    JJim_data = get_object_or_404(SavedPlaces, user =request.user, saved = HP_data)

    JJim_data.delete()
    return redirect("hotplist:profile", HP_author = request.user.id )



@login_required(login_url= 'hotplist:login')
def comment_create(request,HP_id):
    HP = get_object_or_404(HotPlaces, pk = HP_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.place = HP
            review.pub_date = timezone.now()
            review.save()
            update_rating(HP_id)
            return redirect('hotplist:details', HP_id = HP.id)
        else:
            form = ReviewForm(request.POST)
            return render(request,'hotplist/comment_create.html', {'HP': HP, 'form':form})
    else:
        form = ReviewForm()
        return render (request, 'hotplist/comment_create.html',{'HP': HP, 'form':form} )
    

def comment_delete(request, Review_id):
    data = get_object_or_404(Reviews, pk = Review_id)
    data.delete()
    return redirect('hotplist:details', HP_id = data.place.id)



def comment_edit(request, Review_id):
    data = get_object_or_404(Reviews, pk = Review_id)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance = data)
        if form.is_valid():
            edit = form.save(commit = False)
            edit.pub_date = timezone.now()
            edit.save()
            update_rating(data.place.id)
            return redirect("hotplist:details", HP_id = data.place.id)
        else:
            form = ReviewForm(instance=data)
            return render(request, 'hotplist/comment_create.html',{"form":form})
    else:
        form = ReviewForm(instance= data)
        return render(request,'hotplist/comment_create.html', {'form':form})






 
                







