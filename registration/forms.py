import string

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.validators import ASCIIUsernameValidator

from talentalps import constants
from user.models import Candidate, Company

User = get_user_model()

class UserProfileForm(forms.Form):
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    retype_password = forms.CharField(widget=forms.PasswordInput())
    accept_terms = forms.BooleanField(required=False)
    receive_updates = forms.BooleanField(required=False)

    def clean_accept_terms(self):
        accept_terms = self.cleaned_data.get('accept_terms')
        if not accept_terms:
            raise forms.ValidationError("You must read and accept the Terms & Condition and Privacy Policy before registering")

    def clean_password(self):
        password = self.cleaned_data.get('password')
        n = len(password)
        errors = []
        if not any(x.isupper() for x in password):
            errors.append('Password requires at least 1 capital letter.')
        if not any(x.islower() for x in password):
            errors.append('Password requires at least 1 lower case letter.')
        if not any(x.isdigit() for x in password):
            errors.append('Password requires at least 1 digit.')
        if n < 9:
            errors.append('Password needs to be at least 8 characters long.')
        validation_error = "\n".join(errors)
        if errors:
            raise forms.ValidationError(validation_error)
        return password
    
    def clean_retype_password(self):
        retype_password = self.cleaned_data.get('retype_password')
        if retype_password != self.cleaned_data.get('password'):
            raise forms.ValidationError("Passwords do not match")
        return retype_password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered, please use a different email.")
        return email
    
    def clean_name(self):
        return string.capwords(self.cleaned_data.get('name'))

class CandidateRegisterForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ('gender', 'seeking_status')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['seeking_status'].initial = 'active'

class CompanyRegistrationForm(forms.ModelForm):
    
    class Meta:
        model = Company
        fields = ('company_name', 'description', 'website', 'company_size', 'company_type', 'founded', 'industry', 'other_industry', 'address', 'postcode', 'state')