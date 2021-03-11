from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from . import forms
from . import recommendations
from . import read_apple_data
from .models import Member
import decimal

# Create your views here.
def index(request):
	return render(request, 'base.html')

# example object, remove recommendation model and system complete
class ExampleRecommendation:
	name = 'Example Workout'
	embed = 'https://www.youtube.com/embed/1b98WrRrmUs' # example: jumping jacks
	combination = '3x10'
	requires = 'None'

class HomeView(LoginRequiredMixin, TemplateView):
	template_name = "home.html"
	
	# TODO: if user has not provided info, redirect to getinfo

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# TODO: pull this weeks steps from database
		# should be ordered by most recent day last
		s = read_apple_data.StepData(self.request)
		s.save_step_data()
		#context['steps'] = [8020,4630,11880,3025,8432,6448,7976]
		context['steps'] = s.get_recent_steps(7)
		
		# access the user object that is stored in the database
		# note that the django user id and the member user id stored in db are different
		r = recommendations.Recommendation(self.request)
		
		r.make_recommendations()
		context['recommendations'] = r.final_recs
		context['steps recommendation'] = r.step_rec
		return context

class RegisterView(FormView):
	template_name = 'form.html'
	form_class = forms.RegisterForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['step'] = 'Step 1/2'
		context['title'] = 'Create an account'
		context['button_title'] = 'Sign up'
		return context

	def form_valid(self, form):
		form.save()
		reg_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
		login(self.request, reg_user)
		return HttpResponseRedirect(reverse_lazy('getinfo'))

class GetInfoView(LoginRequiredMixin, FormView):
	template_name = 'form.html'
	form_class = forms.MemberForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['step'] = 'Step 2/2'
		context['title'] = "Let's get to know you a bit"
		context['button_title'] = 'Get started'
		return context

	def form_valid(self, form):
		member = form.save(commit=False)
		member.user = self.request.user
		member.save()
		return HttpResponseRedirect(reverse_lazy('home'))

class WorkoutView(LoginRequiredMixin, FormView):
	template_name = 'form.html'
	form_class = forms.WorkoutForm
	success_url = reverse_lazy('home')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Submit Workout Data'
		context['button_title'] = 'Submit'
		return context

	def form_valid(self, form):
		form.instance.user_id = self.request.user.id
		currentMember = Member.objects.get(id=form.instance.user_id)

		# get the exercise name and turn it into the corresponding attributes
		changeDifficulty = form.cleaned_data['workoutName'] + 'Difficulty'
		changePreference = form.cleaned_data['workoutName']

		# use getattr() to access the existing difficulty/preference values
		currentDifficulty = getattr(currentMember, changeDifficulty)
		currentPreference = getattr(currentMember, changePreference)

		# Now, we adjust the difficulty/preference values accordingly
		if form.cleaned_data['workoutDifficulty'] == None: # just right
			pass

		elif form.cleaned_data['workoutDifficulty'] == True: # too difficult
			setattr(currentMember, changeDifficulty, currentDifficulty - decimal.Decimal('0.2'))

		else: # too easy
			setattr(currentMember, changeDifficulty, currentDifficulty + decimal.Decimal('0.2'))

		if form.cleaned_data['workoutPreference'] == None: # neutral
			pass

		elif form.cleaned_data['workoutPreference'] == True: # liked it
			setattr(currentMember, changePreference, currentPreference - decimal.Decimal('0.2'))

		else: # hated it
			setattr(currentMember, changePreference, currentPreference + decimal.Decimal('0.2'))

		currentMember.save()
		form.save()
		return super(WorkoutView, self).form_valid(form)

def thanks(request):
	return render(request, 'thanks.html')

# should prob have this in a different python file
def handle_uploaded_file(f):
	with open('uploaded_files/' + str(f), 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)

# These are the two different forms for steps/strength exercise submissions.
# I've left the default submission with both of them combined to show how it works
# and so you can change the submission page/add urls to your preference.

'''
class StepWorkoutView(LoginRequiredMixin, FormView):
	template_name = 'form.html'
	form_class = forms.WorkoutForm
	success_url = reverse_lazy('home')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Submit Workout Data'
		context['button_title'] = 'Submit'
		return context

	def form_valid(self, form):
		form.instance.user_id = self.request.user.id
		currentMember = Member.objects.get(id=form.instance.user_id)

		# (Note) there is no 'stepPreference' attribute, so only the
		# difficulty attribute is changed
		changeDifficulty = 'stepDifficulty'

		# use getattr() to access the existing difficulty/preference values
		currentDifficulty = getattr(currentMember, changeDifficulty)

		# Now, we adjust the difficulty/preference values accordingly
		if form.cleaned_data['workoutDifficulty'] == None: # just right
			pass

		elif form.cleaned_data['workoutDifficulty'] == True: # too difficult
			setattr(currentMember, changeDifficulty, currentDifficulty - decimal.Decimal('0.2'))

		else: # too easy
			setattr(currentMember, changeDifficulty, currentDifficulty + decimal.Decimal('0.2'))

		currentMember.save()
		form.save()
		return super(StepWorkoutView, self).form_valid(form)

class StrengthWorkoutView(LoginRequiredMixin, FormView):
	template_name = 'form.html'
	form_class = forms.WorkoutForm
	success_url = reverse_lazy('home')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Submit Workout Data'
		context['button_title'] = 'Submit'
		return context

	def form_valid(self, form):
		form.instance.user_id = self.request.user.id
		currentMember = Member.objects.get(id=form.instance.user_id)

		# get the exercise name and turn it into the corresponding attributes
		changeDifficulty = form.cleaned_data['workoutName'] + 'Difficulty'
		changePreference = form.cleaned_data['workoutName']

		# use getattr() to access the existing difficulty/preference values
		currentDifficulty = getattr(currentMember, changeDifficulty)
		currentPreference = getattr(currentMember, changePreference)

		# Now, we adjust the difficulty/preference values accordingly
		if form.cleaned_data['workoutDifficulty'] == None: # just right
			pass

		elif form.cleaned_data['workoutDifficulty'] == True: # too difficult
			setattr(currentMember, changeDifficulty, currentDifficulty - decimal.Decimal('0.2'))

		else: # too easy
			setattr(currentMember, changeDifficulty, currentDifficulty + decimal.Decimal('0.2'))

		if form.cleaned_data['workoutPreference'] == None: # neutral
			pass

		elif form.cleaned_data['workoutPreference'] == True: # liked it
			setattr(currentMember, changePreference, currentPreference - decimal.Decimal('0.2'))

		else: # hated it
			setattr(currentMember, changePreference, currentPreference + decimal.Decimal('0.2'))

		currentMember.save()
		form.save()
		return super(StrengthWorkoutView, self).form_valid(form)
		'''
