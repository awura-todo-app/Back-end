from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserProfileSerializer,RegisterSerializer , LoginSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from .serializers import TaskSerializer
from todos.models import Task
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404


class UserDetailAPI(APIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (AllowAny,)
  def get(self,request,*args,**kwargs):
    user = User.objects.get(id=request.user.id)
    serializer = UserProfileSerializer(user)
    return Response(serializer.data)

class RegisterUserAPIView(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = RegisterSerializer

  def post(self, request, *args, **kwargs):
      response = super().post(request, *args, **kwargs)
      if response.status_code == status.HTTP_201_CREATED:
          return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
      return response

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = []
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = authenticate(request, username=serializer.validated_data['username'],
                                password=serializer.validated_data['password'])
            if user is not None:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}) 

            else:
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class TaskAPIView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self,request,*args,**kwargs):
    tasks = Task.objects.filter(user=request.user)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def post(self, request, *args, **kwargs):
    data = {
        'user': request.user.id,
        'title': request.data.get('title'),
        'description': request.data.get('description'),
        'complete': request.data.get('complete', False),
        'created_at': request.data.get('created_at')  
    }
    serializer = TaskSerializer(data=data)
    if serializer.is_valid():
        serializer.save(user=request.user) 
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class TaskDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id, *args, **kwargs):
        try:
            task = Task.objects.get(id=id)
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response(
                {"res": "Task Doesn't Exist"},
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, id, *args, **kwargs):
        task = get_object_or_404(Task, id=id)
        serializer = TaskSerializer(task)
        task.delete()
        return Response({"response": "Task Deleted", "task": serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request, id, *args, **kwargs):
        try:
            task = Task.objects.get(id=id)
            data = {
                'title': request.data.get('title', task.title),
                'description': request.data.get('description', task.description),
                'complete': request.data.get('complete', task.complete),
                'created_at': request.data.get('created_at', task.created_at)
            }
            serializer = TaskSerializer(instance=task, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Task.DoesNotExist:
            return Response(
                {"res": "Task Doesn't Exist"},
                status=status.HTTP_404_NOT_FOUND
            )
