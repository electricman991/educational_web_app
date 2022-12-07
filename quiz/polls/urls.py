from django.urls import path
from polls.forms import NameForm

from . import views

app_name= 'polls'
urlpatterns = [
    # ex: /polls/
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/<int:question_id>', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('/about', views.about, name='about'),
    #path('save_results/', views.SaveResultsView.as_view, name='save_results'),
    #path('<int:question_id>/answers/', views.answers, name='answers'),
    #path('answers/', views.seeAllAnswers.as_view(), name='allAnswers'),
    
]