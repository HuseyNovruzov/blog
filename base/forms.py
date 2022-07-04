from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from .models import CustomUser, Messages
from django import forms
from mptt.forms import TreeNodeChoiceField

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email','username',)


class UserUpdateForm(ModelForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'user_avatar']

class CommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Messages.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].required = False
        self.fields['parent'].widget.attrs.update(
           {'class': 'd-none'}
        )
        
        self.fields['parent'].label = ''
        
    class Meta:
        model = Messages
        fields = ('body','parent',)
        

        
