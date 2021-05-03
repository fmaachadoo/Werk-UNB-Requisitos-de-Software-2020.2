from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import WerkUser, Workspace, Activity, WerkTask


def homeView(request):
    user = request.user
    if user.is_authenticated:
        CurrentTasks = WerkTask.objects.filter(user=user, done=False)
        DoneTasks = WerkTask.objects.filter(user=user, done=True)

        if request.POST and request.POST.get('action') == 'create-task':
            new_task = WerkTask()
            new_task.user = request.user
            new_task.title = request.POST.get('titulo')
            new_task.body = request.POST.get('corpo')
            new_task.save()
            return redirect("/")

        return render(request, 'home_login.html', {'UserTasks': CurrentTasks, 'DoneTasks': DoneTasks})
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

        new_workspace = Workspace()
        new_workspace.title = 'Area de Trabalho de ' + str(request.POST['first-name'] or 'Usuário')
        new_workspace.save()

        new_archived_workspace = Workspace()
        new_archived_workspace.title = 'Tarefas Arquivadas'
        new_archived_workspace.save()

        new_user = WerkUser()
        new_user.first_name = request.POST['first-name']
        new_user.last_name = request.POST['last-name']
        new_user.email = request.POST['email']
        new_user.username = username
        new_user.password = password
        new_user.workspace_id = new_workspace.id
        new_user.archived_workspace_id = new_archived_workspace.id
        new_user.save()

        login(request, new_user)
        return redirect("/")

    return render(request, 'cadastro.html')


def logoutUser(request):
    user = request.user
    if user.is_authenticated:
        logout(request)

    return redirect('/')



