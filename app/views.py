from django.shortcuts import render
from .forms import ImportForm, RegisterForm
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

# Create your views here.
def index(request):
	return render(request, 'base.html')

class HomeView(TemplateView):
	template_name = "home.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# TODO: pull this weeks steps from database
		context['steps'] = [8020,4630,11880,3025,8432,6448,7976]
		return context

class RegisterView(FormView):
	template_name = 'register.html'
	form_class = RegisterForm
	success_url = '/getinfo'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['step'] = '1/2'
		context['title'] = 'Create an account'
		context['button_title'] = 'Sign up'
		return context


class GetInfoView(FormView):
	template_name = 'register.html'
	form_class = ImportForm
	# success_url = '/login'
	success_url = '/' # redirect to home for now

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['step'] = '2/2'
		context['title'] = "Let's get to know you a bit"
		context['button_title'] = 'Get started'
		return context

def thanks(request):
	return render(request, 'thanks.html')

# should prob have this in a different python file
def handle_uploaded_file(f):
	with open('uploaded_files/' + str(f), 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)


