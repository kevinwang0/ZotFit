from django.shortcuts import render
from .forms import ImportForm
from django.http import HttpResponseRedirect


# Create your views here.
def index(request):
	return render(request, 'base.html')


def getinfo(request):
	print(request.method + "\n\n")
	if request.method == 'POST':
		form = ImportForm(request.POST)
		if form.is_valid():
			print("true")
			return HttpResponseRedirect('/thanks')
		else:
			print("false")
	else:
		form = ImportForm()
	return render(request, 'getinfo.html', {'form':form})

def thanks(request):
	return render(request, 'thanks.html')