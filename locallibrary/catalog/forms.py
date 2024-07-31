import datetime
from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from catalog.models import BookInstance


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
        help_text=_("Enter a date between now and 4 weeks (default 3).")
    )

    def clean_renewal_date(self):
        data = self.cleaned_data["renewal_date"]

        if data < datetime.date.today():
            raise ValidationError(_("Invalid date - renewal in past"))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_("Invalid date - renewal more than 4 weeks ahead"))

        return data


class RenewBookModelForm(ModelForm):
    def clean_due_back(self):
        data = self.cleaned_data["due_back"]
        # Check if a date is not in the past
        if data < datetime.date.today():
            raise ValidationError(_("Invalid date - renewal in past"))
        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_("Invalid date - renewal more than 4 weeks ahead"))
        # Remember to always return the cleaned data.
        return data

    class Meta:
        model = BookInstance
        fields = ["due_back"]
        labels = {"due_back": _("Renewal_date")}
        help_text = {"due_back": _("Enter a date between now and 4 weeks (default 3).")}


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text=_('Required. Enter a valid email address.'))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("The email address is already in use."))
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_("The username is already taken."))
        return username

    def save(self, commit: bool = ...) -> Any:
        return super().save(commit)
