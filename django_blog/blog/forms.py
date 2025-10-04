from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Post, Profile, Comment
from taggit.forms import TagWidget

User = get_user_model()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    profile_picture = forms.ImageField(required=False) #optional upload during signup

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'profile_picture', 'password1', 'password2')

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile  # Access the Profile model via the related name
        fields = ('bio', 'profile_picture')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'tags')
        widgets = {
            'tags': TagWidget(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment...'}),
        }