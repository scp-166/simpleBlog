from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
	path('', views.blog_list, name='blog_list'),
	path('blog_category/<int:blog_category_id>/', views.get_blog_with_category, name='get_blog_with_category'),
	path('date/<int:year>/<int:month>/', views.get_blog_with_date, name='get_blog_with_date'),
	path('<int:blog_pk>/', views.blog_detail, name='blog_detail'),
]


