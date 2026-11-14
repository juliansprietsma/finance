from django.urls import path

from . import views

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profileview'),
    path('profile/password_change', views.ProfilePasswordChangeView.as_view(), name='passwordchangeview'),
    path('profile/email_change', views.ProfileEmailChangeView.as_view(), name='emailchangeview'),
]