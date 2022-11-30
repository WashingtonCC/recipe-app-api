""".
URL mappings for the user API.
"""
from django.urls import path
from user import views


app_name = "user" # userd for reverse('user:create')

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name="create")
]
