"""View module for handling requests about pillars"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from pillarquestapi.models import Pillars
from django.contrib.auth.models import User


class PillarsView(ViewSet):
    """Student able to view all pillars with achievements from quests"""

# get list of all pillars
    def list(self, request):
        """Handle GET requests to pillars resource
        Returns:
            Response -- JSON serialized list of pillars
        """

        # get current user
        current_user = request.auth.user.id

        # get all pillars, then get all pillars with current user's pk as a foreign key
        pillars = Pillars.objects.all()
        if pillars is not None:
            # section in filter is (column in quest table :: what we're matching to in filter)
            current_user_pillars = pillars.filter(user_id=current_user)

        # translate to JSON and respond to client side
        pillars_serializer = PillarsSerializer(
            current_user_pillars, many=True, context={'request': request})

        return Response(pillars_serializer.data)

# make serializer for pillars
class PillarsSerializer(serializers.ModelSerializer):
    """JSON serializer for pillars
    Arguments:
        serializer type
    """
    class Meta:
        model = Pillars
        fields = ('id', 'label')
        depth = 1