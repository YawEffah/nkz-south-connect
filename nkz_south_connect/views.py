from django.shortcuts import render, redirect, get_object_or_404
from connect_admin.models import *
from django.urls import reverse
from django.contrib import messages
from connect_admin.forms import CommentForm
# Create your views here.


def index(request):
    executives = Member.objects.filter(type='executive')[:3]
    current_news = News.objects.filter(is_disabled=False).order_by('-date')[:4]
    projects = Project.objects.all()
    health_projects = Project.objects.filter(type='health').count()
    education_projects = Project.objects.filter(type='education').count()
    other_projects = Project.objects.filter(type='other').count()
    scholarships = Scholarship.objects.all().count()

    context = {
        'executives': executives,
        'current_news': current_news,
        'projects': projects,
        'scholarships': scholarships,
        'health_projects': health_projects,
        'education_projects': education_projects,
        'other_projects': other_projects,
        }
    return render(request, 'nkz_south_connect/index.html', context)


def about_us(request):
    executives = Member.objects.filter(type='executive')

    context = {
        'executives': executives,
        }
    
    return render(request, 'nkz_south_connect/about_us.html', context)


def news(request):
    current_news = News.objects.filter(is_disabled=False)

    context = {
        'current_news': current_news
    }
    return render(request, 'nkz_south_connect/news.html', context)


def news_details(request, news_title):
    news = News.objects.get(title=news_title)
    current_news = News.objects.filter(is_disabled=False).order_by('-date')[:4]

    context = {
        'news': news,
        'current_news': current_news
    }
    return render(request, 'nkz_south_connect/news_details.html', context)


def projects(request):
    projects = Project.objects.all()

    context = {
        'projects': projects
    }
    return render(request, 'nkz_south_connect/projects.html', context)


def project_details(request, project_name):
    project = get_object_or_404(Project, name=project_name)
    projects = Project.objects.all()
    comments = Comment.objects.filter(project=project).order_by('-date')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.project = project
            # Convert 0 rating to None
            if comment.rating == 0:
                comment.rating = None
            comment.save()
            messages.success(request, 'Comment added successfully')
            return redirect(reverse('nkz_south_connect:project_details', args=[project_name]))
    else:
        form = CommentForm()

    context = {
        'project': project,
        'projects': projects,
        'form': form,
        'comments': comments,
    }
    return render(request, 'nkz_south_connect/project_details.html', context)