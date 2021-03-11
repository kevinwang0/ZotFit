from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Member, Workout
import datetime

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
		exclude = ('user', 'squat', 'lunge', 'reverseLunge', 'jumpSquat', 'lateralLunge', 'calfRaise', 
					'singleCalfRaise', 'jumpingJack', 'sealJump', 'inwardCalfRaise', 'gluteBridge',
					'inchworm', 'goodMorning', 'romanianDeadlift', 'quadLegCurl', 'pushup', 'benchDip',
					'pressup', 'plankTap', 'diamondPushup', 'russianTwist', 'situp', 'legRaise', 'deadBug',
					'crunchyFrog', 'reverseSnowAngel', 'superman', 'plankRow', 'lowRow', 'latPulldown', 
					'pullup', 'bicepCurl', 'deadlift', 'hammerCurl', 'medicineBallSlam', 'benchpress',
					'shoulderPress', 'tricepExtension', 'chinup', 'squatDifficulty', 'lungeDifficulty', 
					'reverseLungeDifficulty', 'jumpSquatDifficulty', 'lateralLungeDifficulty', 
					'calfRaiseDifficulty', 'singleCalfRaiseDifficulty', 'jumpingJackDifficulty', 
					'sealJumpDifficulty', 'inwardCalfRaiseDifficulty', 'gluteBridgeDifficulty',
					'inchwormDifficulty', 'goodMorningDifficulty', 'romanianDeadliftDifficulty', 
					'quadLegCurlDifficulty', 'pushupDifficulty', 'benchDipDifficulty', 'pressupDifficulty', 
					'plankTapDifficulty', 'diamondPushupDifficulty', 'russianTwistDifficulty', 'situpDifficulty', 
					'legRaiseDifficulty', 'deadBugDifficulty', 'crunchyFrogDifficulty', 'reverseSnowAngelDifficulty', 
					'supermanDifficulty', 'plankRowDifficulty', 'lowRowDifficulty', 'latPulldownDifficulty', 
					'pullupDifficulty', 'bicepCurlDifficulty', 'deadliftDifficulty', 'hammerCurlDifficulty', 
					'medicineBallSlamDifficulty', 'benchpressDifficulty', 'shoulderPressDifficulty', 
					'tricepExtensionDifficulty', 'chinupDifficulty', 'bodyWeight', 'stepDifficulty', 'latestExerciseRecDate', 
					'latestExerciseRecs', 'latestStepsRecs', 'latestUploadDate')
		labels = {
			'barbell': ('I have access to barbells.'),
			'benchpressEquipment': ('I have access to a bench press.'),
			'dumbbell': ('I have access to a dumbbells.'),
			'pullupBar': ('I have access to a pullup bar.'),
			'medicineBall': ('I have access to a medicine ball.'),
			'resistanceBand': ('I have access to a resistance band.'),
		}
		help_texts = {
			'height': ('In inches'),
		}
		widgets = {
			'birth' : forms.widgets.SelectDateWidget(years=range(1900, 2021)),
			'gender': forms.RadioSelect,
			'goal': forms.RadioSelect,
		}

class WorkoutForm(forms.ModelForm):
	class Meta:
		model = Workout
		exclude = ('user',)
		widgets = {
			'workoutDate' : forms.widgets.SelectDateWidget()
		}
		labels = {
			'workoutDifficulty' : 'How difficult was the workout?',
			'workoutPreference' : 'Did you like the exercise?'
		}
	field_order = ['workoutDate', 'workoutName', 'steps', 'sets', 'reps']


# These are the two different forms for steps/strength exercise submissions.
# I've left the default submission with both of them combined to show how it works
# and so you can change the submission page/add urls to your preference.

'''
class StepWorkoutForm(forms.ModelForm):
	class Meta:
		model = Workout
		exclude = ('user', 'workoutPreference', 'sets', 'reps', 'workoutName')
		widgets = {
			'workoutDate' : forms.widgets.SelectDateWidget()
		}
		labels = {
			'workoutDifficulty' : 'How difficult was the workout?',
		}
	field_order = ['workoutDate', 'sets']

class StrengthWorkoutForm(forms.ModelForm):
	class Meta:
		model = Workout
		exclude = ('user',)
		widgets = {
			'workoutDate' : forms.widgets.SelectDateWidget()
		}
		labels = {
			'workoutDifficulty' : 'How difficult was the workout?',
			'workoutPreference' : 'Did you like the exercise?'
		}
	field_order = ['workoutDate', 'workoutName', 'steps', 'sets', 'reps']
'''

