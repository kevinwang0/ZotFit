from django import forms

class ImportForm(forms.Form):
	height = forms.IntegerField(min_value=0, max_value=120)
	weight = forms.IntegerField(min_value=0, max_value=1500)
	birthday = forms.DateField()

	weightGoals = forms.CharField(widget = forms.Textarea)
