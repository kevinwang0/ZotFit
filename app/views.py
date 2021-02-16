from django.shortcuts import render
from .forms import ImportForm
from django.http import HttpResponseRedirect


# Create your views here.
def index(request):
	return render(request, 'base.html')


def getinfo(request):
	app.read_apple_data.a()
	print(request.method + "\n\n")
	if request.method == 'POST':
		form = ImportForm(request.POST, request.FILES)
		if form.is_valid():
			print("true")
			handle_uploaded_file(request.FILES['healthData'])
			return HttpResponseRedirect('/thanks')
		else:
			print("false")
	else:
		form = ImportForm()
	return render(request, 'getinfo.html', {'form':form})

def thanks(request):
	return render(request, 'thanks.html')

# should prob have this in a different python file
def handle_uploaded_file(f):
	with open('uploaded_files/' + str(f), 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)