from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from django.contrib.auth.models import User
from django.contrib import messages
from .models import WerkUser, WerkTask
from django.template import RequestContext
from datetime import datetime, timezone
from django.core import serializers
from django.utils import timezone


# View homepage
def homeView(request):
    user = request.user
    if user.is_authenticated:
        current_tasks = WerkTask.objects.filter(user=user, done=False, archived=False)
        done_tasks = WerkTask.objects.filter(user=user, done=True, archived=False)

        if request.POST:
            request_action = request.POST.get('action')
            if request_action == 'create-task':
                create_task(request)
            elif request_action == 'finish_task':
                finish_task(request, user)
            elif request_action == 'return_task':
                return_task(request, user)
            elif request_action == 'start_task':
                start_task(request, user)
            elif request_action == 'remove_task':
                remove_task(request, user)
            elif request_action == 'archive_tasks':
                archive_tasks(request, user)

        return render(request, 'home_login.html', {'UserTasks': current_tasks, 'DoneTasks': done_tasks})
    else:
        return render(request, 'home.html')


def remove_task(request, user):
    task = WerkTask.objects.filter(user=user, id=request.POST.get('task_id')).delete()


def start_task(request, user):
    task = WerkTask.objects.get(user=user, id=request.POST.get('task_id'))
    if task.start_time is None:
        task = WerkTask.objects.get(user=user, id=request.POST.get('task_id'))
        task.start_time = timezone.now()


def return_task(request, user):
    task = WerkTask.objects.get(user=user, id=request.POST.get('task_id'))
    if task.done is True:
        task.done = False
        task.end_time = None
        task.save()


def finish_task(request, user):
    task = WerkTask.objects.get(user=user, id=request.POST.get('task_id'))
    if task.end_time is None:
        task.end_time = timezone.now()
        task.done = True
        duration_time = task.end_time - task.start_time
        task.duration = duration_time
        task.save()
        finish_task(request, user)



def create_task(request):
    new_task = WerkTask()
    new_task.user = request.user
    new_task.title = request.POST.get('titulo')
    new_task.body = request.POST.get('corpo')
    new_task.save()

def profileView(request):
    return render(request, 'profile.html')

def loginView(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        # This method of user authentication is deprecated and should not be considered a secure method
        # This project is only for purposes of software engineering learning
        # So, there is no need for it to be a secure project
        user = User.objects.filter(username=username, password=password).first()
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.warning(request, "Email ou Senha incorretos!")
    return render(request, 'login.html')


def cadastroView(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        existing_user = User.objects.filter(username=username, password=password).first()
        if existing_user:
            return render(request, 'cadastro.html')

        new_user = WerkUser()
        new_user.first_name = request.POST['first-name']
        new_user.last_name = request.POST['last-name']
        new_user.email = request.POST['email']
        new_user.username = username
        new_user.password = password
        new_user.save()

        login(request, new_user)
        return redirect("/")

    return render(request, 'cadastro.html')


# Logout do Usuario
def logoutUser(request):
    user = request.user
    if user.is_authenticated:
        logout(request)

    return redirect('/')


# Dashboard View
def dashboardView(request):
    user = request.user
    if user.is_authenticated:
        # These django queries are not optimal and should not be done like that;
        # It has been done this way for sake of faster implementation.
        # A query implementation like that makes the performance really bad.
        response_objects = {
            'done_tasks': WerkTask.objects.filter(user=user, done=False, archived=False),
            'serialized_archived_task_list': serializers.serialize('json', WerkTask.objects.filter(user=user, archived=True)),
            'archived_task_list': WerkTask.objects.filter(user=user, archived=True),
            'archived_task_count': WerkTask.objects.filter(user=user, archived=True).count(),
            'total_task_count': WerkTask.objects.filter(user=user).count(),
            'total_task_elapsed_time': WerkTask.objects.filter(user=user).aggregate(Sum('duration')).get('duration__sum')
        }
        return render(request, 'dashboard.html', response_objects)
