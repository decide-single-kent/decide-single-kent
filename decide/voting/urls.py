from django.urls import path
from . import views


urlpatterns = [
    path('', views.VotingView.as_view(), name='voting'),
    path('<int:voting_id>/', views.VotingUpdate.as_view(), name='voting'),
    path('voting/', views.voting, name='voting'),
    path('new_question/', views.question, name='new_question'),
    path('new_question/close_windows/', views.close, name='close_windows'),
    path('new_auth/', views.auth, name='new_auth'),
]
