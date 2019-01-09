from django import forms
from django.contrib.auth.models import User
from .models import Assignment, Solution, UserProfile
import datetime

# class AlbumForm(forms.ModelForm):
#
#     class Meta:
#         model = Album
#         fields = ['artist', 'album_title', 'genre', 'album_logo']
class SolutionForm(forms.ModelForm):
	class Meta:
		model = Solution
		fields = ['title','body']

	def __init__(self, *args, **kwargs):
		print("#############")
		user = kwargs.pop('user')
		usr_year = UserProfile.objects.get(user=user).year
		course=kwargs.pop('course')
		# print("##############" + str(usr_year))
		# usr_assign = Assignment.objects.filter(year=usr_year)
		super(SolutionForm, self).__init__(*args, **kwargs)
		#self.fields['assignment'].queryset = Assignment.objects.filter(year=usr_year,course__name=course)

class AssignmentForm(forms.ModelForm):
	class Meta:
		model=Assignment
		fields=['num','name','questions','deadline']

class SolCreditForm(forms.ModelForm):
	class Meta:
		model=Solution
		fields=['points','comments']


class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	confirm_password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		help_texts = {
			'username': 'Enter your College Roll No.',
		}
		fields = ['username', 'email', 'password']

	def clean(self):
		cleaned_data = super(UserForm, self).clean()
		password = cleaned_data.get("password")
		confirm_password = cleaned_data.get("confirm_password")

		if password != confirm_password:
			raise forms.ValidationError("password does not match")

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['full_name', 'year',]
