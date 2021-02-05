from django import forms

POSSIBLE_GOALS = [
	('loseWeight', 'Lose weight'),
	('gainMuscle', 'Gain muscle'),
]

class ImportForm(forms.Form):
	height = forms.IntegerField(label = "Height", min_value=0, max_value=120, initial="72")
	weight = forms.IntegerField(label = "Weight", min_value=0, max_value=1500, initial ="160")
	birthday = forms.DateField(label = "Birthday")
	# healthData = forms.FileField(label = "Your health data", upload_to='templates/')
	healthData = forms.FileField(label="Your health data")
	weightGoals = forms.MultipleChoiceField(label = "Some of your health goals", widget = forms.CheckboxSelectMultiple, choices=POSSIBLE_GOALS)
