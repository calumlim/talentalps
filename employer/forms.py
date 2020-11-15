from django import forms

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