from rest_framework import serializers

from .models import Group_project, Learner_project, Poll, Choice, Vote
# from django.contrib.auth.models import User
from users.models import CustomUser

from rest_framework.authtoken.models import Token


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'


class ChoiceSerializer(serializers.ModelSerializer):
    votes = VoteSerializer(many=True, required=False)

    class Meta:
        model = Choice
        fields = '__all__'


class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Poll
        fields = '__all__'

class GroupProjectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group_project
        fields = '__all__'

class LearnerProjectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Learner_project
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ( 'first_name', 'last_name', 'email', 'password', 'promotion')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            promotion=validated_data['promotion'],
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user
