from django import forms
from .models import CustomUser

class AdminSignupForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ("username", "email")

    def save(self, commit=True):
        user = super(AdminSignupForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if commit and password1 and password1 == password2:
            user.set_password(password1)
            user.save()
        return user
