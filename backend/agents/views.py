from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Team
from .serializers import TeamSerializer


class WebhookView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        print("Received webhook data:", data)
        print("Args:", args)
        print("Kwargs:", kwargs)
        return Response({"status": "success"}, status=200)



class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
