from django.urls import path , include 
from rest_framework.routers import DefaultRouter 
from . import views 
#router = DefaultRouter()
#router.register(r'chercheurs', ProjetsListCreateAPIView)

urlpatterns =[
   # path('api/',include(router.urls)),
    path('projects/', views.ProjetsListCreateAPIView.as_view(), name ='projets-create'),
    path('Chercheurs/',views.ChercheurListCreateAPIview.as_view(), name='Chercheur_create'),
    path('Encadrement/', views.EncadrementListCreateAPIview.as_view() , name='encadrement_create'),
    path('Conf_journals/' , views.Conf_journListCreateAPIview.as_view(), name='confJourn_create')
]

