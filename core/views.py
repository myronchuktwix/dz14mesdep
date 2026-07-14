from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, TaskForm, ProfileForm, BioForm
from .models import Task, Profile
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Message



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user=user)
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)
    stats = {'total': tasks.count(), 'done': tasks.filter(done=True).count(), 'active': tasks.filter(done=False).count()}
    return render(request, 'core/dashboard.html', {'stats': stats})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    if request.method == 'POST':
        p_form = ProfileForm(request.POST, instance=request.user)
        b_form = BioForm(request.POST, instance=request.user.profile)
        if p_form.is_valid() and b_form.is_valid():
            p_form.save()
            b_form.save()
            return redirect('profile')
    else:
        p_form = ProfileForm(instance=request.user)
        b_form = BioForm(instance=request.user.profile)
    
    return render(request, 'core/profile.html', {
        'p_form': p_form, 
        'b_form': b_form
    })

def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            t = form.save(commit=False)
            t.user = request.user
            t.save()
            return redirect('tasks')
    else:
        form = TaskForm()
    return render(request, 'core/task_create.html', {'form': form})

def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.done = not task.done
    task.save()
    return redirect('tasks')

@login_required
def task_list(request):
    filter_type = request.GET.get('filter', 'all')
    
    if filter_type == 'active':
        tasks = Task.objects.filter(user=request.user, done=False)
    elif filter_type == 'done':
        tasks = Task.objects.filter(user=request.user, done=True)
    else:
        tasks = Task.objects.filter(user=request.user)
        
    return render(request, 'core/tasks.html', {'tasks': tasks})

@login_required
def user_list(request):
    users = User.objects.exclude(pk=request.user.pk)
    return render(request, 'core/user_list.html', {'users': users})

@login_required
def chat(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)
    if other_user == request.user:
        return redirect('user_list')

    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Message.objects.create(sender=request.user, recipient=other_user, text=text)
            return redirect('chat', user_id=user_id)

    messages = Message.objects.filter(
        Q(sender=request.user, recipient=other_user) | 
        Q(sender=other_user, recipient=request.user)
    )
    return render(request, 'core/chat.html', {'other_user': other_user, 'messages': messages})

@login_required
def inbox(request):
    sent_to = Message.objects.filter(sender=request.user).values_list('recipient', flat=True)
    received_from = Message.objects.filter(recipient=request.user).values_list('sender', flat=True)
    partner_ids = set(sent_to) | set(received_from)
    partners = User.objects.filter(pk__in=partner_ids)

    dialogs = []
    for partner in partners:
        last_msg = Message.objects.filter(
            Q(sender=request.user, recipient=partner) |
            Q(sender=partner, recipient=request.user)
        ).last()
        dialogs.append({'partner': partner, 'last_message': last_msg})

    return render(request, 'core/inbox.html', {'dialogs': dialogs})