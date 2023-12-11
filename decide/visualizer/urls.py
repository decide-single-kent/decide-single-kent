from django.urls import path
from .views import VisualizerView


urlpatterns = [

    path('visualizer/<int:voting_id>/', views.visualizer_view, name='visualizer'),
]
