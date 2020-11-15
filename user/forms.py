from django import forms
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class LogInForm(forms.Form):
    email = forms.EmailField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        try:
            user = authenticate(username=email, password=password)
            if user is not None:
                if user.userprofile.verified:
                    return user
                else:
                    raise forms.ValidationError("Please verify your account before logging in.")
            else:
                raise forms.ValidationError("Email or password is incorrect.")
        except User.DoesNotExist:
            raise forms.ValidationError("Email or password is incorrect.")
        return None

class ResetPasswordEmailForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True)

class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())

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