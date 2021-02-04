from django import forms

class ImportForm(forms.Form):
	height = forms.IntegerField(label = "Height", min_value=0, max_value=120, initial="72")
	weight = forms.IntegerField(label = "Weight", min_value=0, max_value=1500, initial ="160")
	birthday = forms.DateField(label = "Birthday")
	# healthData = forms.FileField(label = "Your health data", upload_to='templates/')
	healthData = forms.FileField(label="Your health data")
	weightGoals = forms.CharField(label = "Some of your health goals", widget = forms.Textarea, initial="Reduce Weight, gain muscle")
