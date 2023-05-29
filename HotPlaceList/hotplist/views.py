from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'hotplist/index.html')

def detail(request):
    hotplace=hotplace.objects.all()