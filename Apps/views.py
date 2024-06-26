from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import todo
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        new_todo = todo(user=request.user, todo_name=task)
        new_todo.save()

    all_todos = todo.objects.filter(user=request.user)
    context = {'todos': all_todos}
    return render(request, 'todo/todo.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(password) < 5:
            messages.error(request, 'Password must be at least 5 characters')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Choose another.')
            return redirect('register')

        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()
        messages.success(request, 'User successfully created, login now')
        return redirect('login')
    return render(request, 'todo/register.html', {})


def LogoutView(request):
    logout(request)
    return redirect('login')


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')

        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect('home-page')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    return render(request, 'todo/login.html', {})


@login_required
def DeleteTask(request, name):
    try:
        todos = todo.objects.filter(user=request.user, todo_name=name)
        
        if todos.exists():
            todos.delete()
            messages.success(request, f'All todos with name "{name}" have been deleted.')
        else:
            messages.error(request, f'Todo "{name}" not found.')
        
    except todo.MultipleObjectsReturned:
        messages.error(request, f'Multiple todos found with name "{name}". Please resolve this issue.')
        
    return redirect('home-page') 


@login_required
def Update(request, name):
    try:
        todo_items = todo.objects.filter(user=request.user, todo_name=name)
        
        if todo_items.exists():
            todo_items.update(status=True)
            
            messages.success(request, f'All todos named "{name}" have been updated to completed.')
        else:
            messages.error(request, f'Todo "{name}" not found.')
        
    except Exception as e:
        messages.error(request, f'Error updating todos named "{name}": {str(e)}')
        
    return redirect('home-page')

