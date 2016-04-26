from django import forms

from django.contrib.auth.forms import ReadOnlyPasswordHashField

from accounts.models import User, RegisteredVehicle, DriversLicense, InsurancePolicy, STATE_CHOICES, PARKING_ZONES
from dlnvalidation import is_valid

import re
import datetime

today = datetime.date.today()

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'date_of_birth','first_name','last_name','is_valet','profile_pic')


    def clean_email(self):
        EMAIL_REGEX = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\b')
        email = self.cleaned_data.get('email')
        email = email.lower()

        try:
            user = User.objects.all().filter(email=email)
            if user:
                raise forms.ValidationError("Sorry, this email has already been registered.")
        except:
            pass

        if not EMAIL_REGEX.match(email):
            raise forms.ValidationError("Invalid email. Please try again.")

        return email

    def clean_first_name(self):
        NAME_REGEX = re.compile(r'\b[a-zA-Z]+$\b')
        first_name = self.cleaned_data.get('first_name')
        if not NAME_REGEX.match(first_name):
            raise forms.ValidationError("Invalid name. Your first name must only include letters.")

        first_name = first_name.capitalize()

        return first_name

    def clean_last_name(self):
        NAME_REGEX = re.compile(r'\b[a-zA-Z]+$\b')
        last_name = self.cleaned_data.get('last_name')
        if not NAME_REGEX.match(last_name):
            raise forms.ValidationError("Invalid name. Your last name must only include letters.")

        last_name = last_name.capitalize() 

        return last_name

    def clean_date_of_birth(self):
        

        dob = self.cleaned_data.get('date_of_birth')
        # dob_datime_obj = datetime.datetime.strptime(dob, '%Y-%m-%d').date() # convert str into datetime.date obj
        print '-------------'
        print type(dob)
        print '-------------'

        if dob >= today:
            raise forms.ValidationError('You must be at least 18 or older to drive. Enter a valid date of birth.')

        difference = today - dob # datetime.timedelta(34)
        days = difference.days
        if days < 6570:
            raise forms.ValidationError("You are not old enough to drive.")

        return dob


    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'date_of_birth', 'first_name','last_name')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


# =================
# Register Vehicle
# =================
class RegisteredVehicleForm(forms.ModelForm):


    class Meta:
        model = RegisteredVehicle
        fields = ('make','model','color','license_plate_number','year','updated_registration_tags','parking_permit_zone','vehicle_pic')


    def clean_make(self):
        
        VEHICLE_REGEX = re.compile(r'[a-zA-Z]+')
        make = self.cleaned_data.get('make')
        if not VEHICLE_REGEX.match(make):

            raise forms.ValidationError("Sorry, we couldn't recognize that brand.")

        return make

    def clean_model(self):
        
        VEHICLE_REGEX = re.compile(r'[a-zA-Z]+')
        model = self.cleaned_data.get('model')
        if not VEHICLE_REGEX.match(model):

            raise forms.ValidationError("Oops, that model didn't match the brand.")

        return model

    def clean_color(self):
        
        COLOR_REGEX = re.compile(r'\b[a-zA-Z]+$\b')
        color = self.cleaned_data.get('color')
        if not COLOR_REGEX.match(color):
            raise forms.ValidationError("Invalid color. Please use alphabetical characters only.")

        return color

    def clean_license_plate_number(self):
        
        LICENSE_REGEX = re.compile(r'')
        plate_number = self.cleaned_data.get('license_plate_number')
        if not LICENSE_REGEX.match(plate_number):

            raise forms.ValidationError("Invalid license plate sequence.")

        return plate_number

    def clean_year(self):
        pass

    def clean_parking_permit_zone(self):
        
        zone = self.cleaned_data.get('parking_permit_zone')
        if zone not in PARKING_ZONES:
            raise forms.ValidationError('There are no permits for this zone. Please select a different option.')

        return zone

# =================
# Drivers License
# =================
class DriversLicenseForm(forms.ModelForm):

    date_of_birth = forms.DateField(label='Date of Birth', widget=forms.TextInput(attrs={'type':'date', 'class':'datepicker', 'placeholder': 'YYYY/MM/DD'})) 

    class Meta:

        model = DriversLicense
        fields = ('legal_first_name', 'legal_last_name', 'date_of_birth', 'license_id_number', 'registered_city', 'registered_state',)


    def clean_legal_first_name(self):
        
        NAME_REGEX = re.compile(r'\b[a-zA-Z]+$\b')
        legal_first_name = self.cleaned_data.get('legal_first_name')
        if not NAME_REGEX.match(legal_first_name):
            raise forms.ValidationError("Invalid name. Your first name must only include letters.")

        legal_first_name = legal_first_name.capitalize()

        return legal_first_name

    def clean_legal_last_name(self):
        
        NAME_REGEX = re.compile(r'\b[a-zA-Z]+$\b')
        legal_last_name = self.cleaned_data.get('legal_last_name')
        if not NAME_REGEX.match(legal_last_name):
            raise forms.ValidationError("Invalid name. Your first name must only include letters.")

        legal_last_name = legal_last_name.capitalize() 

        return legal_last_name

    def clean_date_of_birth(self):
        pass

    def clean_license_id_number(self):
        
        state = self.cleaned_data.get('registered_state')
        license = self.cleaned_data.get('license_id_number')
        if not is_valid(license, state):

            raise forms.ValidationError("License # is not valid for registered state.")

        return license

    def clean_registered_city(self):
        pass

    def clean_registered_state(self):
        
        state = self.cleaned_data.get('registered_state')
        if state not in STATE_CHOICES:

            raise forms.ValidationError("Invalid state. Please choose from the valid state choies.")

        state = state.upper()
        return state

# =================
# Insurance Policy
# =================
class InsurancePolicyForm(forms.ModelForm):

    class Meta:

        model = InsurancePolicy
        fields = ('company', 'policy_number', 'agent_first_name','agent_last_name', 'agent_phone_number')

    def clean_company(self):
        pass

    def clean_policy_number(self):
        pass


    def agent_first_name(self):
        NAME_REGEX = re.compile(r'\b[a-zA-Z]+$\b')
        agent_first_name = self.cleaned_data.get('agent_first_name')
        if not NAME_REGEX.match(agent_first_name):
            raise forms.ValidationError("Invalid name. Your first name must only include letters.")

        agent_first_name = agent_first_name.capitalize()

        return agent_first_name

    def agent_last_name(self):
        NAME_REGEX = re.compile(r'\b[a-zA-Z]+$\b')
        agent_last_name = self.cleaned_data.get('agent_last_name')
        if not NAME_REGEX.match(agent_last_name):
            raise forms.ValidationError("Invalid name. Your first name must only include letters.")

        agent_last_name = agent_last_name.capitalize()

        return agent_last_name

    def agenct_phone_number(self):
        pass

