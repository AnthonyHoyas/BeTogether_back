
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import api_view, permission_classes

from django.shortcuts import get_object_or_404, redirect

from users.models import CustomUser
from .models import Group_project, Learner_project, Poll, Choice

from .serializers import ChangePasswordSerializer, CustomUserSerializer, GroupProjectsSerializer, LearnerProjectsSerializer, PollSerializer, ChoiceSerializer, VoteSerializer, UserSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser   

from django.middleware.csrf import get_token



# this should be gone
class ChoiceList(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = Choice.objects.filter(poll_id=self.kwargs["pk"])
        return queryset
    serializer_class = ChoiceSerializer

    def post(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs["pk"])
        if not request.user == poll.created_by:
            raise PermissionDenied("You can not create choice for this poll.")
        return super().post(request, *args, **kwargs)

# this should be gone
class CreateVote(APIView):
    serializer_class = VoteSerializer

    def post(self, request, pk, choice_pk):
        voted_by = request.data.get("voted_by")
        data = {'choice': choice_pk, 'poll': pk, 'voted_by': voted_by}
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            vote = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# this should be gone
class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def destroy(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs["pk"])
        if not request.user == poll.created_by:
            raise PermissionDenied("You can not delete this poll.")
        return super().destroy(request, *args, **kwargs)

class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer

class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request,):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            print('Succes login')
            return Response({"token": user.auth_token.key})

        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)

# we don't need that now
class CSRFGeneratorView(APIView):
    def get(self, request):
        csrf_token = get_token(request)
        return Response(csrf_token)

class LogoutView(APIView):
    def get(self, request):
        logout(request)
        return redirect('login')

# To get all group projects class based view doesn't work
class GroupProjectsView(APIView):
    serializer_class = GroupProjectsSerializer

    def get(self, request):
        queryset = Group_project.objects.all()
        Group_project = get_object_or_404(queryset, user=request.user)

# To get all group projects
@api_view(('GET',))
@permission_classes((IsAdminUser,))
def get_all_group_projects(request):
    
    if request.method == 'GET':
        gp = Group_project.objects.all()
        serializer = GroupProjectsSerializer(gp, many=True)
        return Response(serializer.data)

# To get group projects by ID

@api_view(('GET',))
@permission_classes((IsAdminUser,))
def get_group_projects_by_id(request, pk):
    if request.method == 'GET':
        gp = Group_project.objects.filter(id=pk)
        serializer = GroupProjectsSerializer(gp, many=True)
        
    return Response(serializer.data)

# To create group projects
@api_view(('POST',))
@permission_classes((IsAdminUser,))  
def create_group_projects(request):
        serializer = GroupProjectsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# To get all learner projects

@api_view(('GET',))
def get_all_learner_projects(request):
    if request.method == 'GET':
        lp = Learner_project.objects.filter()
        serializer = LearnerProjectsSerializer(lp, many=True)
        
    return Response(serializer.data)


# To get all users

@api_view(('GET',))
def get_all_users(request):
    if request.method == 'GET':
        user = CustomUser.objects.filter()
        serializer = CustomUserSerializer(user, many=True)
        
    return Response(serializer.data)    

# To get learner projects by id

@api_view(('GET',))
def get_all_learner_projects_by_id(request, pk):
    if request.method == 'GET':
        lp = Learner_project.objects.filter(id=pk)
        serializer = LearnerProjectsSerializer(lp, many=True)
        
    return Response(serializer.data)

# To get users by id

@api_view(('GET',))
def get_users_by_id(request, pk):
    if request.method == 'GET':
        user = CustomUser.objects.filter(id=pk)
        serializer = CustomUserSerializer(user, many=True)
        
    return Response(serializer.data)

# To create a learner projects
@api_view(('POST',))  
def create_learner_projects(request):
        serializer = LearnerProjectsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# To get own profile and modify it

@api_view(('GET', 'PATCH'))
def get_own_profile_info(request):
    if request.method == 'GET':
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        # user = CustomUser.objects.filter(id)
        serializer = CustomUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# To change password

class ChangePasswordView(generics.UpdateAPIView):

    serializer_class = ChangePasswordSerializer
    model = CustomUser
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)