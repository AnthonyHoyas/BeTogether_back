from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import api_view

from django.shortcuts import get_object_or_404, redirect
from .models import Group_project, Learner_project, Poll, Choice

from .serializers import GroupProjectsSerializer, LearnerProjectsSerializer, PollSerializer, ChoiceSerializer, VoteSerializer, UserSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework import permissions

from django.middleware.csrf import get_token



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
            return Response({"token": user.auth_token.key})

        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class CSRFGeneratorView(APIView):
    def get(self, request):
        csrf_token = get_token(request)
        return Response(csrf_token)

class LogoutView(APIView):
    def get(self, request):
        logout(request)
        return redirect('login')

class GroupProjectsView(APIView):
    serializer_class = GroupProjectsSerializer

    def get(self, request):
        queryset = Group_project.objects.all()
        Group_project = get_object_or_404(queryset, user=request.user)


@api_view(('GET',))
def get_all_group_projects(request):
    if request.method == 'GET':
        gp = Group_project.objects.all()
        serializer = GroupProjectsSerializer(gp, many=True)
        return Response(serializer.data)

@api_view(('GET',))
def get_all_learner_projects(request):
    if request.method == 'GET':
        lp = Learner_project.objects.filter()
        serializer = LearnerProjectsSerializer(lp, many=True)
        return Response(serializer.data)

# class CreateLearnerProject(APIView):
#     serializer_class = LearnerProjectsSerializer

#     def post(self, user, request, pk, choice_pk):
#         data = {'name': name, 'poll': pk, 'voted_by': created_by}
#         serializer = LearnerProjectsSerializer(data=data)
#         if serializer.is_valid():
#             CreateLearnerProject = serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     user =                      models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     name =                      models.CharField(max_length=128)
#     description =               models.TextField
#     database_schema_picture =   models.ImageField(upload_to="images", blank=True, null=True)
#     mockup_picture =            models.ImageField(upload_to="images", blank=True, null=True)
#     group_project = 