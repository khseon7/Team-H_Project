from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Review
from .forms import ReviewForm


# Create your views here.
def index(request):
    return render(request, 'hotplist/index.html')

@login_required(login_url = 'hotplist:login')
def review_create(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            content = form.save(commit = False)
            content.grade = form.save()
            content.pub_date = timezone.now()
            content.author = request.user
            content.save()
            return redirect('hotplist:create')
        else:
            return redirect('hotplist:create')
    else:
        form = ReviewForm()
        return render(request, 'hotplist/detail.html', {'form':form})

@login_required(login_url = "hotplist:login")
def review_delete(request, item_id):
    data = get_object_or_404(ReviewForm, pk = item_id)
    data.delete()
    return render(request, 'hotplist/detail.html')

@login_required(login_url = "hotplist:login")
def review_modify(request, item_id):
    data = get_object_or_404(Review, pk = item_id)
    data.delete()
    return render(request, 'hotplist/detail.html')

# - 로그인 - 진용
# - 맛집등록 - 주호(팀장)
# - 맛집 디테일(댓글,맛집정보,찜하기) - 학선
# - 댓글생성 (평점,작성자,시간 — 가시성(o),수정, 삭제는 작성자만) - 은혜
# - 프로필 정보(찜, 리뷰 리스트)- 선우