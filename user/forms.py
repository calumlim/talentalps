from django import forms
from django.contrib.auth.models import User

class LogInForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].help_text = None
    
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username or password is incorrect.")
        
        return username