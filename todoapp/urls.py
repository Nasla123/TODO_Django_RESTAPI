from django.urls import path
from .views import TodoListApiView,TodoListDetailView

urlpatterns=[
    path("api",TodoListApiView.as_view()),
    path("api/<int:todo_id>",TodoListDetailView.as_view())
]