from django import forms

from accounts.models import User
# ===========
# Login
# ===========

class LoginForm(forms.ModelForm):

	email = forms.EmailField(label='Email', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control',}))
	password = forms.CharField(label='Password', max_length=255, widget=forms.PasswordInput(attrs={'class':'form-control',}))

	class Meta:

		model = User
		fields = ('email', 'password',)