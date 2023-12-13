# voting/forms.py

from django import forms
from .models import Question, QuestionOption, Voting

class VotingForm(forms.ModelForm):
    class Meta:
        model = Voting
        fields = ['name', 'desc', 'question', 'auths']

class QuestionOptionForm(forms.ModelForm):
    class Meta:
        model = QuestionOption
        fields = ['number', 'option']

class QuestionForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Question
        fields = ['desc']

QuestionOptionFormSet = forms.inlineformset_factory(Question, QuestionOption, form=QuestionOptionForm, extra=2, can_delete=False)
