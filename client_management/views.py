from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer
from django.contrib.auth.models import User

class ClientListView(APIView):
    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        user = request.user
        client = Client.objects.create(client_name=data['client_name'], created_by=user)
        serializer = ClientSerializer(client)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ClientDetailView(APIView):
    def get(self, request, pk):
        try:
            client = Client.objects.get(pk=pk)
            serializer = ClientSerializer(client)
            return Response(serializer.data)
        except Client.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            client = Client.objects.get(pk=pk)
            client.client_name = request.data['client_name']
            client.save()
            serializer = ClientSerializer(client)
            return Response(serializer.data)
        except Client.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            client = Client.objects.get(pk=pk)
            client.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Client.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class ProjectCreateView(APIView):
    def post(self, request, client_id):
        try:
            client = Client.objects.get(pk=client_id)
            data = request.data
            user = request.user
            project = Project.objects.create(project_name=data['project_name'], client=client, created_by=user)
            project.users.set(User.objects.filter(id__in=[u['id'] for u in data['users']]))
            serializer = ProjectSerializer(project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Client.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class UserProjectsView(APIView):
    def get(self, request):
        user = request.user
        projects = user.projects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


