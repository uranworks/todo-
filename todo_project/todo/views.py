from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from typing import Optional
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import SignUpForm

@login_required
def task_list(request):
   query: Optional[str] = request.GET.get('q', '')
   tasks = Task.objects.filter(user=request.user, title__icontains=query)
   return render(request, 'todo/task_list.html', {'tasks': tasks, 'query': query})

@login_required
def task_create(request):
   if request.method == 'POST':
      form = TaskForm(request.POST)
      if form.is_valid():
         task = form.save(commit=False)
         task.user = request.user
         task.save()
         return redirect('task_list')
   else:
      form = TaskForm()
   return render(request, 'todo/task_form.html', {'form': form})

@login_required
def task_update(request, task_id):
   task = get_object_or_404(Task, id=task_id, user=request.user)
   if request.method == 'POST':
      form = TaskForm(request.POST, instance=task)
      if form.is_valid():
         form.save()
         return redirect('task_list')
   else:
      form = TaskForm(instance=task)
   return render(request, 'todo/task_form.html', {'form': form})

@login_required
def task_delete(request, task_id):
   task = get_object_or_404(Task, id=task_id, user=request.user)
   task.delete()
   return redirect('task_list')


def signup_view(request):
   if request.method == 'POST':
      form = SignUpForm(request.POST)
      if form.is_valid():
         user = form.save()
         username = form.cleaned_data.get('username')
         messages.success(request, f"Account created for {username}! You can now log in.")
         return redirect('login')
   else:
      form = SignUpForm()

   return render(request, 'registration/signup.html', {'form': form})