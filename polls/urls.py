from .apiviews import LogoutView, PollViewSet, ChoiceList, CreateVote, UserCreate, LoginView
from django.urls import path

from rest_framework.routers import DefaultRouter
# from rest_framework.authtoken import views


router = DefaultRouter()
router.register('polls', PollViewSet, basename='polls')

urlpatterns = [

    path("polls/<int:pk>/choices/", ChoiceList.as_view(), name="choice_list"),
    path("polls/<int:pk>/choices/<int:choice_pk>/vote/", CreateVote.as_view(), name="create_vote"),
    path("users/", UserCreate.as_view(), name="user_create"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),



]   

urlpatterns += router.urls
