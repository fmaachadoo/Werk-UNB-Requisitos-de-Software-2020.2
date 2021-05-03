from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import WerkUser, WerkTask


def homeView(request):
    user = request.user
    if user.is_authenticated:
        current_tasks = WerkTask.objects.filter(user=user, done=False, archived=False)
        done_tasks = WerkTask.objects.filter(user=user, done=True,  archived=False)

        if request.POST:
            request_action = request.POST.get('action')
            if request_action == 'create-task':
                new_task = WerkTask()
                new_task.user = request.user
                new_task.title = request.POST.get('titulo')
                new_task.body = request.POST.get('corpo')
                new_task.save()
                return redirect("/")
            if request_action == 'update_task_status':
                task = request.POST.get('task')

        return render(request, 'home_login.html', {'UserTasks': current_tasks, 'DoneTasks': done_tasks})
    else:
        return render(request, 'home.html')



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


def logoutUser(request):
    user = request.user
    if user.is_authenticated:
        logout(request)

    return redirect('/')



