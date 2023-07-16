from django.urls import path
from .views import UserDetailAPI,RegisterUserAPIView, LoginAPIView,  TaskAPIView, TaskDetailAPIView
urlpatterns = [
  path('detail/',UserDetailAPI.as_view()),
  path('register/',RegisterUserAPIView.as_view()),
  path('login/', LoginAPIView.as_view()),
  path("task/",TaskAPIView.as_view()),
  path("task/<int:id>",TaskDetailAPIView.as_view()),

]

