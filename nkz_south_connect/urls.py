from django .urls import path
from . import views


app_name = 'nkz_south_connect'
urlpatterns = [
    path('', views.index, name='index'),
    path('about-us/', views.about_us, name='about_us'),
    path('news/', views.news, name='news'),
    path('projects/', views.projects, name='projects'),
    path('news_details/<str:news_title>/', views.news_details, name='news_details'),
    path('project_details/<str:project_name>/', views.project_details, name='project_details'),
]