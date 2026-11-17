from django.urls import path

from . import views

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profileview'),
    path('profile/password_change', views.ProfilePasswordChangeView.as_view(), name='passwordchangeview'),
    path('profile/email_change', views.ProfileEmailChangeView.as_view(), name='emailchangeview'),
    path('category/add/', views.add_transaction_category, name='create_category'),
    path('category/<int:pk>/edit', views.edit_category, name='edit_category'),
    path('category/<int:pk>/delete', views.delete_transaction_category, name='delete_category'),
    path('transactions/add/', views.add_transaction, name='create_transaction'),
    path('transactions/<int:pk>/edit/', views.edit_transaction, name="edit_transaction"),
    path('transactions/<int:pk>/delete/', views.delete_transaction, name='delete_transaction'),
]