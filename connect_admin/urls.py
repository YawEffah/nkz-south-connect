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
    path('edit-member/<int:member_id>/update', views.edit_member_view, name='edit_member'),
    path('delete-member/<int:member_id>', views.delete_member, name='delete_member'),
    path('scholarships', views.scholarship_dashboard, name='scholarships'),
    path('scholarship-details/<int:scholarship_id>', views.scholarship_details, name='scholarship_details'),
    path('edit-scholarship/<int:scholarship_id>/update', views.edit_scholarship_view, name='edit_scholarship'),
    path('delete-scholarship/<int:scholarship_id>', views.delete_scholarship, name='delete_scholarship'),
    path('edit-news/<int:news_id>/update', views.edit_news_view, name='edit_news'),
    path('delete-news/<int:news_id>', views.delete_news, name='delete_news'),
    path('edit-project/<int:project_id>/update', views.edit_project_view, name='edit_project'),
    path('delete-project/<int:project_id>', views.delete_project, name='delete_project'),
]