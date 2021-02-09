from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
	first_name = forms.CharField(label = "First name", max_length=30)
	last_name = forms.CharField(label = "Last name", max_length=30)
	email = forms.EmailField(label = "Email")

	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'username')

	# TODO: add new save to actually save data

POSSIBLE_GOALS = [
	('loseWeight', 'Lose weight'),
	('gainMuscle', 'Gain muscle'),
]

class ImportForm(forms.Form):
	height = forms.IntegerField(label = "Height", min_value=0, max_value=120, initial="72")
	weight = forms.IntegerField(label = "Weight", min_value=0, max_value=1500, initial ="160")
	birthday = forms.DateField(label = "Birthday")
	# healthData = forms.FileField(label = "Your health data", upload_to='templates/')
	# healthData = forms.FileField(label="Your health data") # comment out for now
	weightGoals = forms.MultipleChoiceField(label = "Some of your health goals", widget = forms.CheckboxSelectMultiple, choices=POSSIBLE_GOALS)
