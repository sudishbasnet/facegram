from django import forms
from . import models
from django.forms import ModelForm, ClearableFileInput
from facegram.models import User
from django.contrib.auth.forms import UserCreationForm


class UploadPost(forms.ModelForm):
    class Meta:
        model = models.Post
        fields =('title',)


class UploadPostPhoto(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ('photo',)
        widgets = {
            'photo': ClearableFileInput(attrs={'multiple': True}),
        }

class UploadProfile(forms.ModelForm):
    class Meta:
        model = User
        fields =('photo',)


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        unique_together = ('email',)
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2' )
        



class SignUpFormUpdate(forms.ModelForm):
    OPTIONS = (
        ('private','Private'),
        ('public','Public')
        )
    account_type = forms.ChoiceField(required=True, choices=OPTIONS)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','bio','account_type' )
        widgets = {
                'username': forms.TextInput(attrs={'readonly':'readonly'})
            }
