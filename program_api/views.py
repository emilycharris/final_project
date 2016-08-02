from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
import json
from classifieds.models import Program
from program_api.serializers import ProgramSerializer
from program_api.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User

class ProgramListAPIView(generics.ListAPIView):
    queryset = Program.objects.all
    serializer_class = ProgramSerializer
