from django import forms
from .models import Subject, Question, Answer

class NameForm(forms.Form):
    
    
    #fields = ['question_text', 'subject']
    model = Question, Subject
    def get_question(self):
        question = Subject.objects.filter(id=3)
        return question
        
    