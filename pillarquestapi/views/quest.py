"""View module for handling requests about quests"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from pillarquestapi.models import Quest
from django.contrib.auth.models import User
from pillarquestapi.models import pillars

from pillarquestapi.models.pillars import Pillars


class QuestView(ViewSet):
    """Student able to view all current quests on Quest Board"""

# get list of all quests
    def list(self, request):
        """Handle GET requests to quests resource
        Returns:
            Response -- JSON serialized list of quests
        """

        # get current user
        current_user = request.auth.user

        # get all quests, then get all quests with current user's pk as a foreign key
        quests = Quest.objects.all()
        if quests is not None:
            # section in filter is (column in quest table :: what we're matching to in filter)
            current_user_quests = quests.filter(user_id=current_user)

        # translate to JSON and respond to client side
        quests_serializer = QuestsSerializer(
            current_user_quests, many=True, context={'request': request})

        return Response(quests_serializer.data)

# get single quest
    def retrieve(self, request, pk=None):
        """Handle GET requests for single quest
        Returns:
            Response -- JSON serialized quest instance
        """
        try:
            # get current quest using pk
            requested_quest = Quest.objects.get(pk=pk)

            # translate to JSON and respond to the client side
            serializer = QuestsSerializer(
                requested_quest, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

# add new quest
    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized quest instance
        """
        # specify current user
        current_user = request.auth.user
        

       # set up new quest object with user inputs
        try:
            new_quest = Quest.objects.create(
                quest_title=request.data["quest_title"],
                quest_objective=request.data["quest_objective"],
                completed=request.data["completed"],
                user=current_user,
            )
            new_quest.pillars.set(request.data["pillars"])
            # translate to JSON and respond to the client side
            serializer = QuestsSerializer(
                new_quest, context={'request': request})

            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

# delete single quest
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single quest
        Returns:
            Response -- 200, 404, or 500 status code
        """
        # identify quest to delete by pk and call orm
        try:
            quest_to_delete = Quest.objects.get(pk=pk)
            quest_to_delete.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        # send error statuses if method fails
        except quest_to_delete.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# edit single quest
    def update(self, request, pk=None):
        """Handle PUT requests for a quest
        Returns:
            Response -- Empty body with 204 status code
        """

        # specify quest to edit
        quest_to_update = Quest.objects.get(pk=pk)

        # update quest info
        quest_to_update.quest_title = request.data["quest_title"]
        quest_to_update.quest_objective = request.data["quest_objective"]
        # quest_to_update.pillars = request.data["pillars"]
        quest_to_update.completed = request.data["completed"]
        quest_to_update.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

class PillarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pillars
        fields = ('id', 'label')
# make serializer for students
class QuestsSerializer(serializers.ModelSerializer):
    """JSON serializer for students
    Arguments:
        serializer type
    """
    pillars = PillarsSerializer(many = True)
    class Meta:
        model = Quest
        fields = ('id', 'quest_title', 'quest_objective', 'pillars', 'completed')
        depth = 1
