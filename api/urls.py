from django.urls import path
from .views import UserDetailAPI,RegisterUserAPIView, LoginAPIView, TaskList
urlpatterns = [
  path('detail/',UserDetailAPI.as_view()),
  path('register',RegisterUserAPIView.as_view()),
  path('login/', LoginAPIView.as_view()),

]