from django.urls import path
from .views import VisualizerView

urlpatterns = [
    path('visualizer/<int:voting_id>/', VisualizerView.as_view(), name='visualizer'),
    
    
]
