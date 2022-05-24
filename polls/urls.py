from .apiviews import GroupProjectsView, LogoutView, PollViewSet, ChoiceList, CreateVote, UserCreate, LoginView, get_all_group_projects
from django.urls import path

from rest_framework.routers import DefaultRouter

from polls import apiviews
# from rest_framework.authtoken import views


router = DefaultRouter()
router.register('', PollViewSet, basename='index')

urlpatterns = [

    # path("polls/<int:pk>/choices/", ChoiceList.as_view(), name="choice_list"),
    # path("polls/<int:pk>/choices/<int:choice_pk>/vote/", CreateVote.as_view(), name="create_vote"),
    path("users/", UserCreate.as_view(), name="user_create"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("group_projects/all", apiviews.get_all_group_projects, name="group_projects"),
    path("group_projects/<int:pk>", apiviews.get_all_group_projects, name="test"),
    path("learner_projects/all", apiviews.get_all_learner_projects, name="learner_projects"),
    path("learner_projects/<int:pk>", apiviews.get_all_learner_projects, name="learner_projects"),






]   

urlpatterns += router.urls
