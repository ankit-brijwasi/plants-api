from django.urls import path
from nursury.views import NursuryAPIView, plants

urlpatterns = [
    path('plants/', plants),
    path('plants/<int:pk>/', plants),

    path('', NursuryAPIView.as_view()),
    path('<int:pk>/', NursuryAPIView.as_view()),

]
