from django.shortcuts import render,redirect
from .forms import HPForm,ReviewForm
from django.contrib import messages
from .models import HotPlaces, Reviews, SavedPlaces
from django.http import HttpResponse


# Create your views here.
def index(request):
    datas = HotPlaces.objects.all()
    return render(request, 'hotplist/index.html', {'list':datas})


def create(request):
    if request.method == 'POST':
        form = HPForm(request.POST, request.FILES)
        if form.is_valid():
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
    return HttpResponse("Success!")



