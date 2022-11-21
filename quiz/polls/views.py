from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from .models import Subject, Question, Answer, Url
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from .forms import NameForm
from django.views.generic.edit import FormView
import random

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Subject.objects.order_by('-pub_date')[:5]


class DetailView(generic.ListView, FormView):
    model = Subject, Question, Url
    template_name = 'polls/detail.html'
    context_object_name = 'question_list'
    success_url = 'polls:detail/<int:pk>'
    form_class = NameForm
    
    
    def get_queryset(self):
        data = Question.objects.filter(subject=self.kwargs['pk'])
        return data.random(1)

    def get_context_data(self, *args, **kwargs):
        kwargs.update(
            user=self.request.session.get('user', {'is_authenticated': False})
        )
        context = super().get_context_data(*args, **kwargs)

        context['random'] = self.kwargs['random']
        numbers = []
        numbers.append(context['random'])
        print(len(numbers))
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
       
        self.number = random.randint(1, 10)
        if 'next' in self.request.POST:
            
            #data = Url.objects.create(url=self.request.POST['next'], number=self.number)
            #data.save()
            #Url.objects.filter(number=self.number).number 
            
            #print(self.numbers)
            return HttpResponseRedirect(reverse('polls:detail', args=(self.kwargs['pk'], self.number)))
        elif 'submit' in self.request.POST:
            return HttpResponseRedirect(reverse('polls:answers', args=(self.kwargs['pk'],)))
        elif 'previous' in self.request.POST:
            
            Url.objects.filter(url=self.request.POST['previous'], number=self.number)
            return HttpResponseRedirect(reverse('polls:detail', args=(self.kwargs['pk'], self.number)))
            
           # return HttpResponseRedirect(reverse('polls:detail', args=(self.kwargs['pk'], previous)))
            
        #form.get_question()
        return super().form_valid(form)

    
    
class ResultsView(generic.DetailView):
    model = Subject
    template_name = 'polls/results.html'


def answers(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.answer_set.get(pk=request.POST['choice'])
    except (KeyError, Answer.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.answer_text 
        selected_choice.answers = request.POST['answers']
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class seeAllAnswers(generic.DetailView):
    model = Subject
    template_name = 'polls/answers.html'


