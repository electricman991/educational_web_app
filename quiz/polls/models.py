from django.db import models
from django_random_queryset import RandomManager
#import reverse
from django.urls import reverse


# Answers must be written out within 200 characters of text.
# An answer may be pulled randomly for any question as a false answer.
class Subject(models.Model):
    objects = RandomManager()
    subject_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.subject_text


class Question(models.Model):
    objects = RandomManager()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    answers = models.CharField(max_length=200)
    
    def __str__(self):
        return self.question_text + self.answers
    
    def get_absolute_url(self):
        return reverse('polls:detail', kwargs={'pk': self.pk})

class Answer(models.Model):
    objects = RandomManager()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)

    def __str__(self):
        return self.answer_text

    def get_absolute_url(self):
        return reverse('polls:detail', kwargs={'pk': self.question.id, 'pk2': self.pk})

class Choice(models.Model):
    question = models.ForeignKey(Answer, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return self.choice_text 

class Counter(models.Model):
    counter = models.IntegerField(default=0, null=True)

    def __str__(self):
        return str(self.counter)
