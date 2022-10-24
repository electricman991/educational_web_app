from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from .models import Subject, Question, Answer
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Subject.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Subject
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Subject
    template_name = 'polls/results.html'

'''def index(request):
    latest_question_list = Subject.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Subject, pk=question_id)
    #answers = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Subject, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})'''

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
        #selected_choice.answers = request.POST['answer']
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))