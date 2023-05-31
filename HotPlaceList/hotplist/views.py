from django.shortcuts import render,redirect,get_object_or_404
from .forms import HPForm,ReviewForm,UserForm
from django.contrib import messages
from .models import HotPlaces, Reviews, SavedPlaces
from django.http import HttpResponse
from django.utils import timezone



# Create your views here.
##첫 페이지, 맛집 리스트를 화면에 띄움
def index(request):
    datas = HotPlaces.objects.all()
    return render(request, 'hotplist/index.html', {'list':datas})

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


def create(request):
    if request.method == 'POST':
        form = HPForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit = False)
            data.original_rating = data.rating
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

    return render (request, 'hotplist/details.html', {'HP_data':HP_data, 'Review_data':Review_data})



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
    


    def signup(request):
        if request.method == "POST":
            form = UserForm(request.POST)
            if form.is_valid():
                form.save()
                raw_username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password')
                user = authenticate(username = raw_username, password = raw_password)
                
    @login_required(LOGIN_URL = 'hotplist/login')
    def comment_update(request, HP_id):
        return HttpResponse("Hello")







