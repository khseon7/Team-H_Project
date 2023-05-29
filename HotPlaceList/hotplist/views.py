from django.shortcuts import render,redirect
from .forms import HPForm,ReviewForm
from django.contrib import messages


# Create your views here.
def index(request):
    return render(request, 'hotplist/index.html')


def create(request):
    if request.method == 'POST':
        form = HPForm(request.POST, request.FILE)
        if form.is_valid():
            form.save()
            return redirect(request, 'hotplist:index')
        else:
            messages.error(request, "작성 양식에 맞지않습니다. 다시 작성해주세요")
            context = {'form': form}
            return render(request, 'hotplist/create.html',context)
    else:
        form = HPForm()
        return render(request, 'hotplist/create.html',{'form':form})


