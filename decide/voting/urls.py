from django.urls import path
from . import views


urlpatterns = [
    path('', views.VotingView.as_view(), name='voting'),
    path('<int:voting_id>/', views.VotingUpdate.as_view(), name='voting'),
    path('voting/', views.voting, name='voting'),
    path('new_question/', views.question, name='new_question'),
]
