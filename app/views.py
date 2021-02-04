from django.shortcuts import render
from .forms import ImportForm

# Create your views here.
def index(request):
    return render(request, 'base.html')


def import_data(request):
	form = ImportForm()
    return render(request, 'import_data.html', {'form':form})