from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Course
from .forms import LoginForm, RegisterForm, CourseForm
from django.shortcuts import get_object_or_404
from django.conf import settings
import os
from django.core.files.storage import FileSystemStorage

def home(request):
    return render(request, 'home.html')

#@login_required
def course_list(request):
    if request.user.is_authenticated:  # Check if the user is authenticated
        courses = Course.objects.all()
        return render(request, 'course_list.html', {'courses': courses})
    else:
        return render(request, 'course_list.html', {'courses': None}) 

# Admin views
@login_required
def create_course(request):
    if request.method == 'POST':
        course_form = CourseForm(request.POST, request.FILES)
        if course_form.is_valid():
            course = course_form.save(commit=False)  # Create Course object but don't save it to the database yet
            course.save()  # Save the Course object to the database

            # Handle video file
            video_title = request.POST.get('video_title')
            video_file = request.FILES.get('video_file')
            if video_title and video_file:
                fs = FileSystemStorage(location=settings.MEDIA_ROOT + '/videos/')
                video_name = fs.save(video_file.name, video_file)
                course.video_location = 'videos/' + video_name
                course.save()

            # Handle document file
            document_title = request.POST.get('document_title')
            document_file = request.FILES.get('document_file')
            if document_title and document_file:
                fs = FileSystemStorage(location=settings.MEDIA_ROOT + '/docs/')
                document_name = fs.save(document_file.name, document_file)
                course.doc_location = 'docs/' + document_name
                course.save()  # Save the updated Course object to the database

            return redirect('home')  # Redirect after successful course creation
    else:
        course_form = CourseForm()
    return render(request, 'create_course.html', {'course_form': course_form})

def course_detail(request, course_title):
    course = Course.objects.get(title=course_title)
    return render(request, 'course_detail.html', {'course': course})

    

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('create_course') 
                else:
                    return redirect('course_list')  # Replace 'home' with your home page URL name
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Replace 'login' with your login page URL name
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))

@login_required
def delete_course(request, course_title):
    if request.user.is_superuser:
        course = get_object_or_404(Course, title=course_title)
        if request.method == 'POST':
            course.delete()
            return redirect('course_list')
        return render(request, 'delete_course.html', {'course': course})
    else:
        return redirect('course_list')

