from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class BaKetUserCreationForm(UserCreationForm):
    gender = forms.ChoiceField(choices=[('Pria', 'Pria'), ('Wanita', 'Wanita')], required=True, label="Gender")
    birth_date = forms.DateField(required=True, label="Birth Date", widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2', 'birth_date', 'gender']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Save profile picture or other fields in UserProfile
            UserProfile.objects.create(user=user, birth_date=self.cleaned_data.get('birth_date'), gender=self.cleaned_data.get('gender'))
        return user