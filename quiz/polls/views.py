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
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


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
    #test_array = []
    object_list = {}
    object = Question.objects.all()
    context={}
    
    def get_queryset(self):
        data = Question.objects.filter(subject=self.kwargs['pk'])

        #return a random question from the queryset
        return data.random(1)

    def get_context_data(self, **kwargs):
        # get context data that can be used in the template
        context = super().get_context_data(**kwargs)
       
        context['counter'] = Counter.objects.get(pk=1)
        context['choices'] = Choice.objects.all()
        context['questions'] = Question.objects.filter(subject=self.kwargs['pk']).random(10)
        return context

    def form_valid(self, form, *args, **kwargs):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
       
        form = NameForm(self.request.POST)
        
        if 'next' in self.request.POST:
            
            question = get_object_or_404(Question, pk=self.request.POST.get('question'))
            #question = self.test_array[0][0]
            #print(self.test_array)
            #if self.test_array[0]:
                #self.test_array.pop()
            print(question.id)
            print(self.request.POST.get('question'))
            
            if str(question.id) in self.request.POST.get('question'):
                question = get_object_or_404(Question, pk=self.request.POST.get('question'))

            #if question.id == Choice.objects.get(fk=self.request.POST.get('question')).id:
            #print(self.request.POST)
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
                
                if Choice.objects.all().count() >= 10:
                    Choice.objects.all().delete()
                    Counter.objects.filter(pk=1).update(counter=0)
                answer = Answer.objects.get(pk=selected_choice.id)
                
                q = Choice.objects.create(choice_text=selected_choice.answer_text, question=answer)
                q.save()
                
                if selected_choice.answer_text == question.answers:
                    c = Counter.objects.get(pk=1)
                    c.counter += 1
                    c.save()
            
                # Always return an HttpResponseRedirect after successfully dealing
                # with POST data. This prevents data from being posted twice if a
                # user hits the Back button.

                if Choice.objects.all().count() >= 10:
                    
                
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
                    Counter.objects.filter(pk=1).update(counter=0)

                answer = Answer.objects.get(pk=selected_choice.id)
                q = Choice.objects.create(choice_text=selected_choice.answer_text, question=answer)
                q.save()

                if selected_choice.answer_text == question.answers:
                    c = Counter.objects.get(pk=1)
                    c.counter += 1
                    c.save()
                # Always return an HttpResponseRedirect after successfully dealing
                # with POST data. This prevents data from being posted twice if a
                # user hits the Back button.
                return HttpResponseRedirect(reverse('polls:results', args=(self.kwargs['pk'],) ))

            
        return super().form_valid(form)

    
    
class ResultsView(generic.DetailView):
    model = Subject
    template_name = 'polls/results.html'
   

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['counter'] = Counter.objects.get(pk=1)
        context['choice'] = Choice.objects.all()
        context['question'] = Question.objects.get(pk=self.kwargs['pk'])


        return context

    '''def form_valid(self, form, *args, **kwargs):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form=NameForm(self.request.GET)
        print(self.request.GET)
        
        if 'retry' in self.request.GET:
            return HttpResponseRedirect(reverse('polls:detail', args=(self.kwargs['pk'],)))
        
        return super().form_valid(form)'''

'''class SaveResultsView(LoginRequiredMixin, generic.ListView):
    model = Counter
    template_name = 'polls/save.html'
    success_url = reverse_lazy('polls:save_results')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form) 

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['counter'] = Counter.objects.get(pk=1)
        context['choice'] = Choice.objects.all()
        context['question'] = Question.objects.get(pk=self.kwargs['pk'])
        
        return context

    def get_queryset(self):
        return Counter.objects.get(pk=1)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)''' 


def about(request):

    return render(request, 'polls/about.html', {'title': 'About'})
    


    




