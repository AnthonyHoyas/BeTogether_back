
from itertools import groupby
from operator import itemgetter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import api_view, permission_classes

from django.shortcuts import get_object_or_404, redirect

from users.models import CustomUser
from .models import Group_project, Groups, Learner_project, Poll, Choice, Promotion, User_per_promotion, Vote_list

from .serializers import (    
    ChangePasswordSerializer,
    CustomUserSerializer,
    GroupProjectsSerializer,
    GroupSerializer, 
    LearnerProjectsSerializer, 
    PollSerializer, 
    ChoiceSerializer,
    PromotionSerializer,
    UserPerGroupSerializer,
    UserPerPromotionSerializer, 
    VoteListSerializer, 
    VoteSerializer, 
    UserSerializer
)
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



# To create a voting list
@api_view(('POST',))  
def create_vote_list(request):
        serializer = VoteListSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# To get all vote list

@api_view(('GET',))
def get_all_vote_list(request):
    if request.method == 'GET':
        list = Vote_list.objects.filter()
        serializer = VoteListSerializer(list, many=True)
        
    return Response(serializer.data) 


# To get all promotion

@api_view(('GET',))
def get_all_promotion(request):
    if request.method == 'GET':
        list = Promotion.objects.filter()
        serializer = PromotionSerializer(list, many=True)
        
    return Response(serializer.data) 

# To get all users per promotion

@api_view(('GET',))
def get_all_users_per_promotion(request):
    if request.method == 'GET':
        list = User_per_promotion.objects.filter()
        serializer = UserPerPromotionSerializer(list, many=True)
        
    return Response(serializer.data) 








new_dict_from_get_in_view = {}


@api_view(('GET',))
def sort(request):
    if request.method == 'GET':
        lista = Vote_list.objects.filter()
        serializer = VoteListSerializer(lista, many=True)
        dataFromServer = serializer.data
        #print(dataFromServer)

        for i in dataFromServer:
            UserIDFromRaw = i['voted_by']
            WishlistFromRaw = i['whishlist']

            #print(UserIDFromRaw, WishlistFromRaw )
            new_dict_from_get_in_view[UserIDFromRaw] = WishlistFromRaw
        

        for i, users in enumerate(new_dict_from_get_in_view):
            print(i, users)
            n_o_g_n = i/3
        print('number of groups =', round(n_o_g_n)) 

        #this should be looped
        listofvalue = []
        listOf1 = []
        listOf2 = []
        listOf3 = []
        listOf4 = []
        listOf5 = []
        listOf6 = []

        ListOfGroup = []


        for i in (new_dict_from_get_in_view): #get all in data from users
            my_list = new_dict_from_get_in_view[i] 
            my_dict = dict() #make a new dictionary to give project id a value
            for index,value in enumerate(my_list):
                my_dict[index] = value

                if value == '1' and value in my_list:
                    listOf1.append(index)
                elif '1' not in my_list:
                    listOf1.append(1)
                if value == '2' and value in my_list:
                    listOf2.append(index)
                elif '2' not in my_list:
                    listOf2.append(1)
                if value == '3' and value in my_list:
                    listOf3.append(index)
                elif '3' not in my_list:
                    listOf3.append(1)
                if value == '4' and value in my_list:
                    listOf4.append(index)
                elif '4' not in my_list:
                    listOf4.append(1)
                if value == '5' and value in my_list:
                    listOf5.append(index)
                elif '5' not in my_list:
                    listOf5.append(1)
                if value == '6' and value in my_list:
                    listOf6.append(index)
                elif '6' not in my_list:
                    listOf6.append(1)
        sumof6 = {'id':6, 'value': sum(listOf6) }
        sumof5 = {'id':5, 'value': sum(listOf5) }
        sumof4 = {'id':4, 'value': sum(listOf4) }
        sumof3 = {'id':3, 'value': sum(listOf3) }
        sumof2 = {'id':2, 'value': sum(listOf2) }
        sumof1 = {'id':1, 'value': sum(listOf1) }

        listofvalue.append(sumof1)
        listofvalue.append(sumof2)
        listofvalue.append(sumof3)
        listofvalue.append(sumof4)
        listofvalue.append(sumof5)
        listofvalue.append(sumof6)

        print(listofvalue) 


        newlist = sorted(listofvalue, key=itemgetter('value')) 
        newlist2 = newlist[:(round(n_o_g_n))]
        idofprojectwekeep = []

        for i in newlist2:
            idofprojectwekeep.append((i['id']))

        print('id of the project we keep', idofprojectwekeep)  

        #replace all the other id of project by 0
        print(new_dict_from_get_in_view)
        for i in (new_dict_from_get_in_view):
            listOfArray = new_dict_from_get_in_view[i]
            for x in listOfArray:
                    print(x)
                    #print(x, listOfArray)

                    if x != str(idofprojectwekeep[0]) and x != str(idofprojectwekeep[1]):
                        print('?')
                        listOfArray = list(map(lambda items: items.replace(x , '0'), listOfArray))
                        print(listOfArray)

            if listOfArray[0] != '0':
                ListOfGroup.append({'userID': i, 'learner_project': listOfArray[0]})
                print(i, listOfArray[0])
            elif listOfArray[1] != '0':
                ListOfGroup.append({'userID': i, 'learner_project': listOfArray[1]})

                print(i, listOfArray[1])
            elif listOfArray[2] != '0':
                ListOfGroup.append({'userID': i, 'learner_project': listOfArray[2]})

                print(i, listOfArray[2])
            elif listOfArray[3] != '0':
                ListOfGroup.append({'userID': i, 'learner_project': listOfArray[3]})

                print(i, listOfArray[3])
            elif listOfArray[4] != '0':
                ListOfGroup.append({'userID': i, 'learner_project': listOfArray[4]})

                print(i, listOfArray[4])


        OrderedListOfGroup = sorted(ListOfGroup, key=itemgetter('learner_project'))
        #print(OrderedListOfGroup)

        # define a fuction for key
        def key_func(k):
            return k['learner_project']
        
        # sort OrderedListOfGroup data by 'company' key.
        OrderedListOfGroup = sorted(OrderedListOfGroup, key=key_func)

        for key, value in groupby(OrderedListOfGroup, key_func):
            group1 = list(value)
            break

        for key, value in groupby(OrderedListOfGroup, key_func):
            group2 = list(value)


        #print(group1)
        #print(group2)

        for i in group1:
            print(i)
            valueOfLearnerProject1 = i['learner_project']
            break

        for i in group2:
            print(i)
            valueOfLearnerProject2 = i['learner_project']
            break

        valueOfUserInGroup1 = []
        for i in group1:
            print(i)
            valueOfUserInGroup1.append(i['userID'])

        valueOfUserInGroup2 = []
        for i in group2:
            print(i)
            valueOfUserInGroup2.append(i['userID'])

    print(valueOfLearnerProject1)
    print(valueOfLearnerProject2)
    print(valueOfUserInGroup1)
    print(valueOfUserInGroup2)

    #MAKE A GROUP    

    dataisend1 = {'name': "groupOfStudent_1", 'group_project': '1', 'learner_project': valueOfLearnerProject1}
    serializerOfGroup1 = GroupSerializer(data=dataisend1, partial=True)
    #dataisend2 = {'name': "groupOfStudent_2", 'group_project': '1', 'learner_project': valueOfLearnerProject2}
    #serializerOfGroup2 = GroupSerializer(data=dataisend2, partial=True)
    if serializerOfGroup1.is_valid():
        serializerOfGroup1.save() #and serializerOfGroup2.save()
        #return Response(serializerOfGroup1.data, status=status.HTTP_201_CREATED)



    #GET ID FOR GROUPS
    listb = Groups.objects.filter()
    serializerOfGroup1 = GroupSerializer(listb, many=True)
    data_from_new_group = serializerOfGroup1.data
    for i in data_from_new_group:
        print(i)
        GroupIDFromRaw = i['id']
        print(GroupIDFromRaw)


    #MAKE USER PER GROUP
    
    dataisend3 = {'groups':GroupIDFromRaw, 'user': valueOfUserInGroup1}
    serializerOfUserPerGroup = UserPerGroupSerializer(data=dataisend3, partial=True)
    if serializerOfUserPerGroup.is_valid():
        serializerOfUserPerGroup.save()
        return Response(serializerOfUserPerGroup.data, status=status.HTTP_201_CREATED)
    return Response(serializerOfUserPerGroup.errors,  status=status.HTTP_400_BAD_REQUEST)



    return Response(serializer.data) 


#seeallgroups

@api_view(('GET',))
def get_all_groups(request):
    if request.method == 'GET':
        list = Groups.objects.filter()
        serializer = GroupSerializer(list, many=True)
        
    return Response(serializer.data) 