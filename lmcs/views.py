from django.shortcuts import render
from rest_framework.views import APIView
from .models import Projet ,Chercheur ,Encadrement,Conf_journal ,Utilisateur
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import ProjetListSerializer,ConfJournalCreat,EncadrementCreatSerializer,ProjetCreatSerializer ,ProjetDetailSerializer,ChercheurCreat,EncadrementListSerializer,EncadrementDetailSerializer ,ChercheurDetailSerializer ,ChercheurListSerializer  ,ConfJournalListSerializer ,ConfJournalDetailSerializer
from rest_framework import generics , permissions, status
from django.contrib.auth import authenticate, login ,logout
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model



#class RegisterUser(APIView):
  #  permission_classes = [AllowAny]

   # def post(self, request):
   #     serializer = UtilisateurSerializer(data=request.data)
   #     if serializer.is_valid():
   #         serializer.save()
    #        return Response(serializer.data, status=status.HTTP_201_CREATED)
     #   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ProjetListAPIview(generics.ListAPIView):
    queryset = Projet.objects.all()
    serializer_class = ProjetListSerializer

class ProjetDetailAPIview(generics.RetrieveAPIView):
    queryset = Projet.objects.all()
    serializer_class = ProjetDetailSerializer

class ProjetCreatAPIview(generics.CreateAPIView):
    queryset = Projet.objects.all()
    serializer_class = ProjetCreatSerializer

class EncadrementListAPIview(generics.ListAPIView):
    queryset=Encadrement.objects.all()
    serializer_class=EncadrementListSerializer    

class EncadrementDetailAPIview(generics.RetrieveAPIView):
    queryset = Encadrement.objects.all()
    serializer_class = EncadrementDetailSerializer
  
class EncadrementCreatAPIview(generics.CreateAPIView):
    queryset = Encadrement.objects.all()
    serializer_class = EncadrementCreatSerializer

class ChercheurListAPIview(generics.ListAPIView):
    queryset = Chercheur.objects.all()
    serializer_class = ChercheurListSerializer

class ChercheurDetailAPIview(generics.RetrieveAPIView):# for show details for each chercheur 
    queryset = Chercheur.objects.all()
    serializer_class = ChercheurDetailSerializer

class ChercheurCreatAPIview(generics.CreateAPIView):
    queryset=Chercheur.objects.all()
    serializer_class=ChercheurCreat



class ConfJournalListAPIview(generics.ListAPIView): #pour gerer l'affichage de la list des confjournal 
    queryset = Conf_journal.objects.all()
    serializer_class = ConfJournalListSerializer

class ConfJournalDetailAPIview(generics.RetrieveAPIView):# for show details for each chercheur 
    queryset = Conf_journal.objects.all()
    serializer_class = ConfJournalDetailSerializer 
    
class ConfJournalCreatAPIview(generics.CreateAPIView):
    queryset = Conf_journal.objects.all()
    serializer_class = ConfJournalCreat


