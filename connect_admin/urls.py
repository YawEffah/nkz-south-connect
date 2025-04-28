from django.urls import path 

from . import views

app_name = "connect_admin"
urlpatterns = [
    path('', views.admin_dashboard, name='dashboard'),
    path('dashboard', views.admin_dashboard, name='dashboard'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('news', views.news_dashboard, name='news'),
    path('projects', views.projects_dashboard, name='projects'),
    path('members', views.members_dashboard, name='members'),
    path('member-details/<str:member_id>', views.member_details, name='member_details'),
    path('delete_member/<int:member_id>', views.delete_member, name='delete_member'),
    path('edit_news/<int:news_id>', views.edit_news_view, name='edit_news'),
    path('delete_news/<int:news_id>', views.delete_news, name='delete_news'),
    path('edit_project/<int:project_id>', views.edit_project_view, name='edit_project'),
    path('delete_project/<int:project_id>', views.delete_project, name='delete_project'),
]