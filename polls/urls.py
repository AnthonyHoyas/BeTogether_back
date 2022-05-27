from .apiviews import GroupProjectsView, LogoutView, PollViewSet, ChoiceList, CreateVote, UserCreate, LoginView, get_all_group_projects
from django.urls import path
from polls import apiviews

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('', PollViewSet, basename='index')

urlpatterns = [

    # path("polls/<int:pk>/choices/", ChoiceList.as_view(), name="choice_list"),
    # path("polls/<int:pk>/choices/<int:choice_pk>/vote/", CreateVote.as_view(), name="create_vote"),
    path("register/", UserCreate.as_view(), name="user_create"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("group_projects/all", apiviews.get_all_group_projects, name="group_projects"),
    path("group_projects/<int:pk>", apiviews.get_group_projects_by_id, name="group_projects_byid"),
    path("group_projects/new", apiviews.create_group_projects, name="new_group_projects"),


    path("learner_projects/all", apiviews.get_all_learner_projects, name="learner_projects"),
    path("learner_projects/new", apiviews.create_learner_projects, name="new_learner_projects"),
    path("learner_projects/<int:pk>", apiviews.get_all_learner_projects_by_id, name="learner_projects_byid"),

    path("users/<int:pk>", apiviews.get_users_by_id, name="users_byid"),
    path("users/all", apiviews.get_all_users, name="users_show_all"),
    path("users/profile", apiviews.get_own_profile_info, name="current_user"),
    path("users/profile/password", apiviews.ChangePasswordView.as_view(), name="change_password"),

    path("users/profile/vote_list/new", apiviews.create_vote_list, name="new_vote_list"),
    path("users/profile/vote_list/all", apiviews.get_all_vote_list, name="vote_list_show_all"),

    path("usersperpromotion", apiviews.get_all_users_per_promotion, name="user_per_promotion_show_all"),
    path("promotion/all", apiviews.get_all_promotion, name="promotion_show_all")

]   

urlpatterns += router.urls
