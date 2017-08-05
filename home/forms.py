from django import forms
from django.core.validators import RegexValidator


class SubscriptionForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': "Enter Your Email"})
    )
    mobile_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '1234567890'. Up to 15 digits allowed."
    )
    number = forms.CharField(
        validators=[mobile_regex],
        widget=forms.TextInput(attrs={'placeholder': "Enter your Phone Number"})
    )
