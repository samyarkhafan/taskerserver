from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Task
from .serializers import TaskSerializer
import datetime
# Create your views here.


@api_view(['GET'])
def getRoutes(request):
    if request.method == 'GET':
        return Response({
                        'api/v1/login/ and api/v1/logout/': 'For the browsable api auth.',
                        'api/v1/auth/ and api/v1/auth/token/login or /logout': 'For authentication.',
                        'api/v1/tasks/': 'Create a new task or get all the tasks.',
                        'api/v1/tasks/today/': 'Get all of today\'s tasks.',
                        'api/v1/tasks/undone/': 'Get all undone tasks.',
                        'api/v1/tasks/<id>/': 'Read, update, delete a task.',
                        }, status=200)
    else:
        return Response(status=405)


@api_view(['POST', 'GET'])
def crTasks(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            serializer = TaskSerializer(
                data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            else:
                return Response(serializer.errors, status=400)
        elif request.method == 'GET':
            tasks = Task.objects.filter(user=request.user)
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response(status=405)
    else:
        return Response(status=401)


@api_view(['GET', 'PUT', 'DELETE'])
def rudTasks(request, taskid):
    if request.user.is_authenticated:
        if request.method == 'GET':
            try:
                task = Task.objects.get(id=taskid)
            except:
                return Response(status=404)
            else:
                if task.user == request.user:
                    serializer = TaskSerializer(task)
                    return Response(serializer.data, status=200)
                else:
                    return Response(status=403)
        elif request.method == 'PUT':
            try:
                task = Task.objects.get(id=taskid)
            except:
                return Response(status=404)
            else:
                if task.user == request.user:
                    serializer = TaskSerializer(
                        task, request.data, context={"request": request})
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=200)
                    else:
                        return Response(serializer.errors, status=400)
                else:
                    return Response(status=403)
        elif request.method == 'DELETE':
            try:
                task = Task.objects.get(id=taskid)
            except:
                return Response(status=404)
            else:
                if task.user == request.user:
                    task.delete()
                    return Response(status=204)
                else:
                    return Response(status=403)
        else:
            return Response(status=405)
    else:
        return Response(status=401)


@ api_view(['GET'])
def getTodaysTasks(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            tasks = Task.objects.filter(
                user=request.user, activates_on=datetime.date.today())
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response(status=405)
    else:
        return Response(status=401)


@ api_view(['GET'])
def getUndoneTasks(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            tasks = Task.objects.filter(
                user=request.user, activates_on__lt=datetime.date.today())
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response(status=405)
    else:
        return Response(status=401)
