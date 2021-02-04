from django import forms

class ImportForm(forms.Form):
	height = forms.IntegerField()
	weight = forms.IntegerField()
	weightGoals = forms.CharField(widget = forms.Textarea)
