from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from . import forms
from . import recommendations
# from . import read_apple_data
from .models import Member, Workout
from .read_apple_data import StepData
import decimal
# for upload
import zipfile
import os

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
		# get last 7 reported steps (most recent last)
		# TODO: duplicate handling
		workouts = Workout.objects.filter(user=self.request.user).exclude(steps__isnull=True).order_by('-workoutDate')[:7]
		dates = [w.workoutDate for w in workouts]
		steps = [w.steps for w in workouts]
		dates.reverse()
		steps.reverse()
		print("workouts", workouts, "dates", dates, "steps", steps)

		context['labels'] = dates
		context['steps'] = steps
		
		# access the user object that is stored in the database
		# note that the django user id and the member user id stored in db are different
		r = recommendations.Recommendation(self.request)
		r.make_recommendations()

		# context['recommendations'] = r.final_recs
		context['recommendations'] = [ExampleRecommendation(),ExampleRecommendation(),ExampleRecommendation()]
		context['step_rec'] = r.step_rec
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

class StepWorkoutView(LoginRequiredMixin, FormView):
	template_name = 'form.html'
	form_class = forms.StepWorkoutForm
	success_url = reverse_lazy('home')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Submit Step Data'
		context['button_title'] = 'Submit'
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		currentMember = Member.objects.get(user=form.instance.user)

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
	form_class = forms.StrengthWorkoutForm
	success_url = reverse_lazy('home')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Submit Workout Data'
		context['button_title'] = 'Submit'
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		currentMember = Member.objects.get(user=form.instance.user)

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

class UploadFileView(LoginRequiredMixin, FormView):
	template_name = "form.html"
	form_class = forms.UploadFileForm
	success_url = 'home'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Upload Health Data'
		context['button_title'] = 'Upload'
		context['file'] = True
		return context

	def post(self, request, *args, **kwargs):
		# form_class = self.get_form_class()
		form = self.form_class(request.POST, request.FILES)
		upload = request.FILES['healthData']
		print('upload',upload)
		print('upload.chunks', upload.chunks())
		if form.is_valid():
			z = zipfile.ZipFile(upload)
			print('z', z.namelist())
			export = 'apple_health_export/export.xml'
			if export in z.namelist():
				dest_path = './uploads/user_' + str(request.user.id) + '/export.xml'
				os.makedirs(os.path.dirname(dest_path), exist_ok=True)
				with open(dest_path, 'wb+') as dest:
					print('saving to:', dest_path) 
					# write export.xml from zip file
					dest.write(z.read(export))
					print('saving to db...')
					step_data = StepData(request)
					step_data.save_step_data()
			return self.form_valid(form)
		else:
			return self.form_invalid(form)
		return self.form_valid(form)