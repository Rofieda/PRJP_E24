from rest_framework import serializers 
from .models import Chercheur , Projet , Encadrement ,Conf_journal

class ProjetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projet
        fields = '__all__'

class ChercheurSerializer(serializers.ModelSerializer):
    class Meta: 
        model =Chercheur 
        fields='__all__'

class EncadrementSerializer(serializers.ModelSerializer):
    class Meta: 
        model =Encadrement
        fields='__all__'

class Conf_journalSerializer(serializers.ModelSerializer):
    class Meta:
        model=Conf_journal
        fields='__all__'

