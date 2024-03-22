from django.urls import path , include 
from rest_framework.routers import DefaultRouter 
from . import views 

#router = DefaultRouter()
#router.register(r'chercheurs', ProjetsListCreateAPIView)

urlpatterns =[
   
    path('ChercheursList/', views.ChercheurListAPIview.as_view(), name='Chercheur_list'),  # Chercheur list API endpoint
    path('ChercheursList/<int:pk>/', views.ChercheurDetailAPIview.as_view(), name='Chercheur_detail'),
    path('ProjetsList/', views.ProjetListAPIview.as_view(), name='Projet_list'),  # Projet list API endpoint
    path('ProjetsList/<int:pk>/', views.ProjetDetailAPIview.as_view(), name='Projet_detail'),  # Projet detail API endpoint
    path('EncadrementsList/', views.EncadrementListAPIview.as_view(), name='Encadrement_list'),  # Encadrement list API endpoint
    path('EncadrementsList/<int:pk>/', views.EncadrementDetailAPIview.as_view(), name='Encadrement_detail'),  # Encadrement detail API endpoint
    path('Conf_journalsList/', views.ConfJournalListAPIview.as_view(), name='Conf_journal_list'),  # Conf_journal list API endpoint
    path('Conf_journalsList/<int:pk>/', views.ConfJournalDetailAPIview.as_view(), name='Conf_journal_detail'),  # Conf_journal detail API endpoint
    path('ChercheurCreat/' , views.ChercheurCreatAPIview.as_view() , name ='ChercheurCreat'),
    path('ConfJournalCreat/', views.ConfJournalCreatAPIview.as_view(), name='ConfJournalCreat'),
    path('ProjetCreat/',views.ProjetCreatAPIview.as_view(),name='ProjetCreat'),
    path('EncadrementCreat/',views.EncadrementCreatAPIview.as_view(),name='EncadrementCreat')



]
    

