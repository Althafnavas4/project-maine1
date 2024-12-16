from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm
from .models import ShoeSize
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))




class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))










class ShoeSizeForm(forms.Form):
    size = forms.ChoiceField(choices=[])
    
    def __init__(self, shoe_sizes, *args, **kwargs):
        super(ShoeSizeForm, self).__init__(*args, **kwargs)
        size_choices = [(size.id, size.size) for size in shoe_sizes]
        self.fields['size'].choices = size_choices