from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('list-users/', views.ListUserView.as_view()),
    path('change-password/', views.ChangePasswordView.as_view()),

]