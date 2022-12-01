from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from .models import Subject, Question, Answer, Choice, Counter
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from .forms import NameForm
from django.views.generic.edit import FormView, UpdateView
import random


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Subject.objects.order_by('-pub_date')[:5]

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        print(Question.objects.filter(subject=1).random(1).get(subject_id=1))
        context['question'] = Question.objects.filter(subject=1).random(1).get(subject_id=1)
        return context


class DetailView(generic.ListView, FormView):
    model = Question, Subject, Answer, Choice
    template_name = 'polls/detail.html'
    context_object_name = 'question_list'
    success_url = 'answers'
    form_class = NameForm
    test_array = []
    object_list = {}
    object = Question.objects.all()
    context={}
    
    def get_queryset(self):
        data = Question.objects.filter(subject=self.kwargs['pk'])
        #new_question = data.random(1)
       # print(new_question)
        #Choice.objects.create(new_question=new_question)
        
        '''if new_question in self.test_array:
            new_question = data.random(1)
        self.test_array.append(new_question)'''
        
        '''same = False
        while same == False:
            new_question = data.random(1)
            if new_question in self.test_array:
                same = False
            else:
                self.test_array.append(new_question)
                same = True'''

        #print(len(self.test_array))
        return data.random(1)

    def form_valid(self, form, *args, **kwargs):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
       
       
        form = NameForm(self.request.POST)
        
        if 'next' in self.request.POST:
            
            question = get_object_or_404(Question, pk=self.request.POST['question'])
            print(question.id)
            print(self.request.POST.get('question'))
            if str(question.id) in self.request.POST.get('question'):
                question = get_object_or_404(Question, pk=self.request.POST.get('question'))

            #if question.id == Choice.objects.get(fk=self.request.POST.get('question')).id:

            try:
                
                selected_choice = question.answer_set.get(pk=self.request.POST.get('choice'))
                #print(selected_choice)
            except (KeyError, Answer.DoesNotExist):
                # Redisplay the question voting form.
                return render(self.request, 'polls/detail.html', {
                    'question': question,
                    'error_message': "You didn't select a choice.",
                })
            else:
                #print("bye")
                if Choice.objects.all().count() >= 10:
                    Choice.objects.all().delete()
                    Counter.objects.filter(pk=1).update(counter=0)
                answer = Answer.objects.get(pk=selected_choice.id)
                #print(self.request.POST.get('choice'))
                q = Choice.objects.create(choice_text=selected_choice.answer_text, question=answer)
                q.save()
                #point = get_object_or_404(Choice, question_id=self.request.POST['choice'])
                #print(selected_choice.answer_text)
                #print(question.answers)
                if selected_choice.answer_text == question.answers:
                    c = Counter.objects.get(pk=1)
                    c.counter += 1
                    c.save()
            
                # Always return an HttpResponseRedirect after successfully dealing
                # with POST data. This prevents data from being posted twice if a
                # user hits the Back button.

                if Choice.objects.all().count() >= 10:
                    del self.test_array[:]
                
                    return HttpResponseRedirect(reverse('polls:results', args=(self.kwargs['pk'], )))

            return HttpResponseRedirect(reverse('polls:detail', args=(self.kwargs['pk'], self.request.POST.get('question'))))
        
        elif 'submit' in self.request.POST:

            question = get_object_or_404(Question, pk=self.request.POST['question'])

            try:
                
                selected_choice = question.answer_set.get(pk=self.request.POST['choice'])
                print(selected_choice)

            except (KeyError, Answer.DoesNotExist):
                # Redisplay the question voting form.
                return render(self.request, 'polls/detail.html', {
                    'question': question,
                    'error_message': "You didn't select a choice.",
                })
            else:
                
                if Choice.objects.all().count() >= 10:
                    Choice.objects.all().delete()
                answer = Answer.objects.get(pk=selected_choice.id)
                q = Choice.objects.create(choice_text=selected_choice.answer_text, question=answer)
                q.save()
                # Always return an HttpResponseRedirect after successfully dealing
                # with POST data. This prevents data from being posted twice if a
                # user hits the Back button.
                return HttpResponseRedirect(reverse('polls:results', args=(self.kwargs['pk'],) ))

        elif 'retry' in self.request.POST:

            return HttpResponseRedirect(reverse('polls:detail', args=(self.kwargs['pk'],)))

        elif 'previous' in self.request.POST:
            
            return HttpResponseRedirect(reverse('polls:detail', args=(self.kwargs['pk'],)))
            
        return super().form_valid(form)

    
    
class ResultsView(generic.DetailView):
    model = Subject
    template_name = 'polls/results.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['counter'] = Counter.objects.get(pk=1)
        context['choice'] = Choice.objects.all()
        
        
        return context

class seeAllAnswers(generic.DetailView):
    model = Subject
    template_name = 'polls/answers.html'
    


    




