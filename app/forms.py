from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Member

class RegisterForm(UserCreationForm):
	first_name = forms.CharField(label = "First name", max_length=30)
	last_name = forms.CharField(label = "Last name", max_length=30)
	email = forms.EmailField(label = "Email")

	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'username')

	def save(self, commit=True):
		# call Django user save then add other fields
		user = super(RegisterForm, self).save(commit=False)

		user.email = self.cleaned_data["email"]
		user.first_name = self.cleaned_data["first_name"]
		user.last_name = self.cleaned_data["last_name"]
		if commit:
		    user.save()

		return user

class MemberForm(forms.ModelForm):
	class Meta:
		model = Member
		exclude = ('user',)
		labels = {
			'dumbbells': ('I have access to dumbbells.'),
			'benchpress': ('I have access to a bench press.'),
			'squatrack': ('I have access to a squat rack.'),
		}
		help_texts = {
			'height': ('In inches'),
		}
		widgets = {
			'gender': forms.RadioSelect,
			'goal': forms.RadioSelect,
		}

