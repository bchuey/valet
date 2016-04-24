from django import forms


from payments.models import PaymentMethod


class AddPaymentMethodForm(forms.Form):

	cc_full_name = forms.CharField(max_length=100, label='Name on Card', widget=forms.TextInput(attrs={'data-stripe':'name'}))
	cc_number = forms.CharField(max_length=20, label='Credit Card #', widget=forms.TextInput(attrs={'data-stripe':'number'}))
	cc_cvc = forms.CharField(max_length=4, label='CVC', widget=forms.TextInput(attrs={'data-stripe':'cvc'}))
	cc_exp_month = forms.CharField(max_length=2, label='Expiration Month', widget=forms.TextInput(attrs={'data-stripe':'exp-month','placeholder':'e.g. 04'}))
	cc_exp_year = forms.CharField(max_length=4, label='Expiration Year', widget=forms.TextInput(attrs={'data-stripe':'exp-year','placeholder':'e.g. 2019'}))

class UpdatePaymentMethodForm(forms.ModelForm):

	# customer_stripe_id = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'disabled':True}))
	# is_active = forms.BooleanField()
	# is_primary = forms.BooleanField()

	class Meta:

		model = PaymentMethod
		fields = ('customer_stripe_id', 'is_active', 'is_primary')
		widgets = {
			'customer_stripe_id': forms.TextInput(attrs={'disabled':True}),
		}


