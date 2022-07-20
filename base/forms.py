from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import CustomUser, Messages, Articles
from django import forms
from mptt.forms import TreeNodeChoiceField
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email','username',)


class UserUpdateForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'user_avatar', 'bio']

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
        

class ArticleForm(ModelForm):
    class Meta:
        model = Articles
        exclude = ('likes',)
        widgets = {
            'description': SummernoteWidget(),
        }
        