from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import WerkUser, Workspace, Activity, WerkTask
from django.template import RequestContext
from datetime import datetime
from django.utils import timezone


def homeView(request):
    user = request.user
    if user.is_authenticated:
        CurrentTasks = WerkTask.objects.filter(user=user, done=False)
        DoneTasks = WerkTask.objects.filter(user=user, done=True)

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

#Logout do Usuario
def logoutUser(request):
    user = request.user
    if user.is_authenticated:
        logout(request)

    return redirect('/')


#Adicionar Tarefa
def addTask(request):
    user = request.user
    if request.POST:
        if user.is_authenticated:
            new_task = WerkTask()
            new_task.user = request.user
            new_task.title = request.POST['titulo']
            new_task.body = request.POST['corpo']

            #Salvar Task
            new_task.save()

        return redirect("/")

#Deletar Tarefa
def removeTask(request, id):
    user = request.user
    if request.POST:
        if user.is_authenticated:
            task = WerkTask.objects.filter(user=user, id=id).delete()
    return redirect("/") 


#Iniciar hora da tarefa
def startTask(request, id):
    user = request.user
    if request.POST:
        if user.is_authenticated:
            task = WerkTask.objects.get(user=user, id=id)
            if task.start_time is None:
                task.start_time = datetime.now()
                task.save()
    
    return redirect("/")


#Terminar tarefa
def finishTask(request, id):
    user = request.user
    if request.POST:
        if user.is_authenticated:
            task = WerkTask.objects.get(user=user, id=id)
            if task.end_time is None:
                task.end_time = datetime.now()
                task.done = True
                task.save()
                finishTask(request, id)
            else:
                temp = task.end_time - task.start_time
                task.total_time = temp
                task.save()

    
    return redirect("/")

#continuar tarefa
def returnTask(request, id):
    user = request.user
    if request.POST:
        if user.is_authenticated:
            task = WerkTask.objects.get(user=user, id=id)
            if task.done is True:
                task.done = False
                task.start_time = None
                task.end_time = None
                task.save()
    return redirect("/")
