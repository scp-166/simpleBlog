from django.urls import path
from . import views


app_name = 'targetauth'

urlpatterns = [
	path('login/', views.LoginView.as_view(), name='login'),
	path('logout/', views.logout, name='logout'),
	path('token/', views.token),
]