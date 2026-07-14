from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('tasks/', views.task_list, name='tasks'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/toggle/<int:task_id>/', views.toggle_task, name='toggle_task'),
    path('messages/', views.inbox, name='inbox'),
    path('messages/users/', views.user_list, name='user_list'),
    path('messages/<int:user_id>/', views.chat, name='chat'),
]