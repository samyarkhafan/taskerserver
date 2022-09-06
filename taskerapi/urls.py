from django.urls import path
from . import views
urlpatterns = [
    path('', views.getRoutes),
    path('tasks/', views.crTasks),
    path('tasks/today/', views.getTodaysTasks),
    path('tasks/undone/', views.getUndoneTasks),
    path('tasks/<int:taskid>/', views.rudTasks),
]
