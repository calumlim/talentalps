from django import forms

from user import models as user_models
from talentalps import constants

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(required=True)

class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=(forms.PasswordInput()), required=True)
    confirm_password = forms.CharField(widget=(forms.PasswordInput()), required=True)

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
    
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")

        return confirm_password

class CompanyCreateForm(forms.ModelForm):
    logo_x = forms.FloatField(required=False, widget=(forms.HiddenInput()))
    logo_y = forms.FloatField(required=False, widget=(forms.HiddenInput()))
    logo_w = forms.FloatField(required=False, widget=(forms.HiddenInput()))
    logo_h = forms.FloatField(required=False, widget=(forms.HiddenInput()))
    header_x = forms.FloatField(required=False, widget=(forms.HiddenInput()))
    header_y = forms.FloatField(required=False, widget=(forms.HiddenInput()))
    header_w = forms.FloatField(required=False, widget=(forms.HiddenInput()))
    header_h = forms.FloatField(required=False, widget=(forms.HiddenInput()))

    class Meta:
        model = user_models.Company
        fields = ['avatar', 'header_image', 'company_name', 'description', 'website',
        'company_size', 'company_type', 'founded', 'industry', 'other_industry', 'address',
        'postcode', 'state', 'country']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['other_industry'].required = False
        self.fields['website'].required = False
        self.fields['industry'] = forms.MultipleChoiceField(choices=constants.INDUSTRY)
        self.fields['country'].initial = 'MY'
    
    def clean_industry(self):
        return ', '.join(self.cleaned_data.get('industry'))