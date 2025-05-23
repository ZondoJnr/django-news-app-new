from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Article, Newsletter, Publisher, JournalistProfile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'publisher']
        widgets = {
            'publisher': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['publisher'].required = False
        self.fields['publisher'].queryset = Publisher.objects.all()

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['title', 'body', 'publisher']
        widgets = {
            'publisher': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['publisher'].required = False
        self.fields['publisher'].queryset = Publisher.objects.all()

class JournalistProfileForm(forms.ModelForm):
    class Meta:
        model = JournalistProfile
        fields = ['bio', 'photo']

class PublisherUpdateForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ['name', 'bio', 'photo']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
