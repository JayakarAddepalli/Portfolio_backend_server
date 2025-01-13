from django.urls import path
from .views import *

urlpatterns = [
    path('api/csrf/', csrf, name='csrf'),
    path('api/feedback/', FeedbackView.as_view(), name='feedback'),
    path('showusersfeedback/', ShowFeedbackUI, name='show_users_feedback'),
    path('userfeedback/', download_feedback_excel, name='user_feedback')
]
