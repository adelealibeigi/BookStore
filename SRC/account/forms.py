from .models import User,Address

from django import forms
from django.contrib.auth.forms import UserCreationForm


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        if not user.is_superuser:
            self.fields['username'].disabled = True
            self.fields['email'].disabled = True

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name'
        ]


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CheckoutForm(forms.Form):
    state = forms.CharField(label='استان',widget=forms.TextInput(attrs={'style': 'text-align:right;'}))
    city = forms.CharField(label='شهر',widget=forms.TextInput(attrs={'style': 'text-align:right;'}))
    detail_address = forms.CharField(label='نشانی پستی',widget=forms.TextInput(attrs={'style': 'text-align:right;'}))
    code = forms.CharField(label="کد پستی",widget=forms.TextInput(attrs={'style': 'text-align:right;'}))
    phone_number = forms.CharField(label="شماره تماس",widget=forms.TextInput(attrs={'style': 'text-align:right;'}))