from .views import MotivationalQuoteView
from django.urls import path

app_name = 'quotes'

urlpatterns = [
    path('', MotivationalQuoteView.as_view(), name='random-quote'),
]
