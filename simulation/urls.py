from django.urls import path
from .views import index, SimulationListCreateView, SimulationDetailView, SimulationStepView, WeatherView

urlpatterns = [
    path('', index, name='index'),
    path('simulations/', SimulationListCreateView.as_view()),
    path('simulations/<uuid:id>/', SimulationDetailView.as_view()),
    path('simulations/<uuid:id>/step/', SimulationStepView.as_view()),
    path('weather/', WeatherView.as_view()),
]