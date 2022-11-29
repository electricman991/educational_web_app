from django import forms
from .models import Subject, Question, Answer




class NameForm(forms.Form):
    
    model = Question, Subject
    def get_question(self):
        question = Subject.objects.filter(id=3)
        return question
    #submit= forms.CharField(widget=forms.TextInput(attrs={'type': 'submit', 'value': 'Submit', 'name': 'submit'}))
    #next = forms.CharField(widget=forms.TextInput(attrs={'type': 'submit', 'value': 'Next', 'name': 'next'}))
        
    