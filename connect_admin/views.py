from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from .models import *
from django.contrib.auth.models import User
from .forms import  NewsForm, LoginForm, ProjectForm, MemberForm
from django.db.models import Sum
from django.db.models import Count, Q


# Create your views here.


def is_administrator(user):
    return user.groups.filter(name='administrator').exists()

def is_content_manager(user):
    return user.groups.filter(name='content-manager').exists()


def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('connect_admin:dashboard'))

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Signed in successfully')
                return redirect(reverse('connect_admin:dashboard'))
            else:
                # Invalid credentials
                messages.error(request, 'Invalid credentials')
                return render(request, 'connect_admin/login.html', {
                    'form': form
                })
    else:
        form = LoginForm()

    return render(request, 'connect_admin/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.error(request, 'You have been logged out')
    return redirect(reverse('connect_admin:login'))


def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect(reverse('connect_admin:login'))
    
    completed_projects = Project.objects.filter(status='completed').count()
    ongoing_projects = Project.objects.filter(status='ongoing').count()
    total_projects = Project.objects.count()
    context = {
        'completed_projects': completed_projects,
        'ongoing_projects': ongoing_projects,
        'total_projects': total_projects,
        'local_scholarships': Scholarship.objects.filter(type='local').count(),
        'foreign_scholarships': Scholarship.objects.filter(type='foreign').count(),
        'total_scholarships': Scholarship.objects.count(),
    }
    return render(request, 'connect_admin/dashboard.html', context)


def news_dashboard(request):
    current_news = News.objects.filter(is_disabled=False).order_by('-date')[:4]
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'News added successfully')
            return redirect(reverse('connect_admin:news'))
        else:
            messages.error(request, 'An error occurred. Please try again')
            return render(request, 'connect_admin/news_dashboard.html', {'form':form, 'current_news': current_news})
    else:
        form = NewsForm()

    return render(request, 'connect_admin/news_dashboard.html', {'form': form, 'current_news': current_news})


def projects_dashboard(request):
    projects = Project.objects.all()
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the project
            project = form.save()  # This now handles images via the custom save() in ProjectForm
            
            messages.success(request, 'Project added successfully!')
            return redirect(reverse('connect_admin:projects'))
        else:
            messages.error(request, 'An error occurred. Please check the form.')
            return render(request, 'connect_admin/projects_dashboard.html', {
                'form': form,
                'projects': projects,
            })
    
    # GET request: render the form
    form = ProjectForm()
    return render(request, 'connect_admin/projects_dashboard.html', {
        'projects': projects,
        'form': form,
    })

def members_dashboard(request):
    # Get the member_id from the query parameters, if provided
    member_id = request.GET.get('member_id')

    # Base query for accepted members
    members_query = Member.objects.filter(status='accepted')

    # Filter by member_id if provided
    if member_id:
        members_query = members_query.filter(member_id=member_id)

    # Perform aggregations for total members and gender counts
    statistics = Member.objects.aggregate(
        total_members=Count('id'),
        number_of_males=Count('id', filter=Q(gender='Male')),
        number_of_females=Count('id', filter=Q(gender='Female'))
    )

    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            print(form)
            form.save()
            messages.success(request, 'Member added successfully')
            return redirect(reverse('connect_admin:members'))
        else:
            messages.error(request, 'An error occurred. Please try again')
            return render(request, 'connect_admin/members_dashboard.html', {
               'form': form,
                'members': members_query,
                'total_members': statistics['total_members'],
                'number_of_males': statistics['number_of_males'],
                'number_of_females': statistics['number_of_females'],
                'member_id_filter': member_id,  # Include for template reference
            })
    else:
        form = MemberForm()

    context = {
        'form': form,
        'members': members_query,
        'total_members': statistics['total_members'],
        'number_of_males': statistics['number_of_males'],
        'number_of_females': statistics['number_of_females'],
        'member_id_filter': member_id,  # Include for template reference
    }
    return render(request, 'connect_admin/members_dashboard.html', context)



def member_details(request, member_id):
    member = get_object_or_404(Member, member_id=member_id)
    return render(request, 'connect_admin/member_details.html', {'member': member})


def delete_member(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    member.delete()
    messages.success(request, 'Member deleted successfully')
    return redirect(reverse('connect_admin:members'))


def edit_news_view(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, 'News updated successfully!')
            return redirect(reverse('connect_admin:news'))
    else:
        form = NewsForm(instance=news)
    return render(request, 'connect_admin/edit_news.html', {'news':news, 'form': form})


def delete_news(request, news_id):
    project = get_object_or_404(News, pk=news_id)
    project.delete()
    messages.success(request, 'News deleted successfully')
    return redirect(reverse('connect_admin:news'))


def edit_project_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully!')
            return redirect(reverse('connect_admin:projects'))
    else:
        form = ProjectForm(instance=project)
    return render(request, 'connect_admin/edit_project.html', {'project':project, 'form': form})


def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    project.delete()
    messages.success(request, 'Project deleted successfully')
    return redirect(reverse('connect_admin:projects'))
