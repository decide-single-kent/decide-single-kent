# voting/forms.py

from django import forms

from base.models import Auth

from .models import Question, QuestionOption, Voting

class VotingForm(forms.ModelForm):
    class Meta:
        model = Voting
        fields = ['name', 'desc', 'question', 'auths']

class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['desc']

QuestionOptionFormSet = forms.inlineformset_factory(Question, QuestionOption, fields=['number', 'option'], can_delete=False)

class AuthForm(forms.ModelForm):
    class Meta:
        model = Auth 
        fields = ['name', 'url', 'me']
