from django.urls import path
from nursury.views import NursuryAPIView

urlpatterns = [
    path('', NursuryAPIView.as_view()),
    path('<int:pk>/', NursuryAPIView.as_view()),
]
