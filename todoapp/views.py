from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from .serializers import TodoSerializer
from .models import Todo
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class TodoListDetailView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get_object(self,todo_id,user_id):
        try:
            return Todo.objects.get(id=todo_id,user=user_id)
        except Todo.DoesNotExist:
            return None

    def get(self,request,todo_id):
        todo_instance=self.get_object(todo_id,request.user.id)
        if not todo_instance:
            return Response(
                {"res":"Object with to_do id doesnot exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer=TodoSerializer(todo_instance)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,todo_id):
        todo_instance=self.get_object(todo_id,request.user.id)
        if not todo_instance:
            return Response(
                {"res":"Object with todo_id doesnot exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data={
            "task":request.data.get('task'),
            "completed":request.data.get('completed'),
            "user":request.user.id
        }
        serializer=TodoSerializer(instance=todo_instance,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST )
    def delete(self,request,todo_id):
        todo_instance=self.get_object(todo_id,request.user.id)
        if not todo_instance:
            return Response(
                {"res":"Object with todo_id doesnot exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        todo_instance.delete()
        return Response(
            {"res":"Object deleted!"},
            status=status.HTTP_200_OK
        )



class TodoListApiView(APIView):
    permission_classes= [permissions.IsAuthenticated]

    def get(self,request):
        todos=Todo.objects.all().filter(user=request.user.id)
        serializer=TodoSerializer(todos,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request):
        data={
            "task":request.data.get('task'),
            "completed":request.data.get('completed'),
            "user":request.user.id
        }
        serializer=TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

