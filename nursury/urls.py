from django.urls import path
from nursury.views import NursuryView

urlpatterns = [
    path('', NursuryView.as_view()),
    path('<int:pk>', NursuryView.as_view()),
]