from . import views
from django.urls import path

urlpatterns = [
    path('', views.getPrediction.as_view(), name='getPrediction'),
    path('make-prediction/', views.makePrediction.as_view(), name='makePrediction'),
    # path('form/', views.addItem.as_view(), name='getItem')
]