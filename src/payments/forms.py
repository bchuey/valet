from django import forms


from payments.models import PaymentMethod


class AddPaymentMethodForm(forms.Form):

	cc_full_name = forms.CharField(max_length=100, label='Name on Card', widget=forms.TextInput(attrs={'data-stripe':'name'}))
	cc_number = forms.CharField(max_length=20, label='Credit Card #', widget=forms.TextInput(attrs={'data-stripe':'number'}))
	cc_cvc = forms.CharField(max_length=4, label='CVC', widget=forms.TextInput(attrs={'data-stripe':'cvc'}))
	cc_exp_month = forms.CharField(max_length=2, label='Expiration Month', widget=forms.TextInput(attrs={'data-stripe':'exp-month','placeholder':'e.g. 04'}))
	cc_exp_year = forms.CharField(max_length=4, label='Expiration Year', widget=forms.TextInput(attrs={'data-stripe':'exp-year','placeholder':'e.g. 2019'}))

class UpdatePaymentMethodForm(forms.ModelForm):



	class Meta:

		model = PaymentMethod
		fields = ('is_active', 'is_primary')
		