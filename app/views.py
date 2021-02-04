from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'base.html')

def login(request):
	if request.method == 'POST':
		form = ImportForm(request.POST)
		if form.is_valid():
			return render(request, 'NEW_UNCREATED_HTML.html', {'form':form})
		else:
			form = ImportForm()
	return render(request, 'login.html')
