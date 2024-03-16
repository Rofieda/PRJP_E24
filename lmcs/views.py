from django.shortcuts import render
from rest_framework.views import APIView
from .models import Projet ,Chercheur ,Encadrement,Conf_journal
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import ProjetsSerializer ,ChercheurSerializer , EncadrementSerializer ,Conf_journalSerializer
from rest_framework import generics


class ProjetsListCreateAPIView(generics.ListCreateAPIView):
    queryset=Projet.objects.all()
    serializer_class=ProjetsSerializer
#hendle listing chercheurs  ,each chercheur detail informations , adding new chercheur  
    

class ChercheurListCreateAPIview(generics.ListCreateAPIView):
    queryset=Chercheur.objects.all()
    serializer_class=ChercheurSerializer

class EncadrementListCreateAPIview(generics.ListCreateAPIView):
    queryset=Encadrement.objects.all()
    serializer_class=EncadrementSerializer


class Conf_journListCreateAPIview(generics.ListCreateAPIView):
    queryset=Conf_journal.objects.all()
    serializer_class=Conf_journalSerializer


#class Conf_journalListCreateAPIview(generics.ListCreateAPIView):
#    queryset=Conf_journal.objects.all()
#    serializer_class=Conf_journalSerializer


