from django.urls import path

from . import views

app_name= 'polls'
urlpatterns = [
    # ex: /polls/
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('/<int:pk>/answers/', views.seeAllAnswers.as_view(), name='answers'),
    path('answers/', views.seeAllAnswers.as_view(), name='allAnswers')
]