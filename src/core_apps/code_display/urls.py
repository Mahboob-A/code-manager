

from django.urls import path 

from core_apps.code_display.views import QuestionDetailAPIView, QuestionListAPIView

urlpatterns = [
    path('all/', QuestionListAPIView.as_view(), name='api_all_questions'), 
    path('<uuid:id>/', QuestionDetailAPIView.as_view(), name='api_single_question'), 
]
