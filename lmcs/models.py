from django.db import models

class Projet(models.Model):
    id_projet=models.AutoField(primary_key=True)
    titre_projet=models.CharField(max_length=50)
    chef_de_projet=models.CharField(max_length=50)
    domaine=models.CharField(max_length=50)
    annee_debut=models.IntegerField(db_column='année_debut')
    annee_fin=models.IntegerField(db_column='année_fin')
    class Meta :
        db_table ='projets'


class Chercheur(models.Model):
    id_chercheur=models.AutoField(primary_key=True)
    nom_chercheur=models.CharField(max_length=50,null=False)
    prenom_chercheur=models.CharField(max_length=50,null=False)
    etablissement=models.CharField(max_length=50)
    diplome=models.CharField(max_length=100 , choices=[('Licence', 'Licence'), ('Master', 'Master'), ('Ingéniorat', 'Ingéniorat'), ('Doctorat', 'Doctorat'), ('Diplôme d''Études Supérieures', 'Diplôme d''Études Supérieures'), ('Diplôme de Formation Approfondie', 'Diplôme de Formation Approfondie'), ('Diplôme d''Études Approfondies', 'Diplôme d''Études Approfondies'), ('Autre', 'Autre')],null=False)
    email=models.EmailField(unique=True,null=False)
    tel=models.CharField(max_length=50,null=False)
    dblp_lien=models.CharField(max_length=50)
    research_gate_lien=models.CharField(max_length=50)
    google_scholar_lien=models.CharField(max_length=50)
    site_web=models.CharField(max_length=50)
    grade_ensignement=models.CharField(max_length=50, choices=[('Professeur', 'Professeur'), ('MCA', 'MCA'), ('MCB', 'MCB'), ('MAA', 'MAA'), ('MAB', 'MAB'), ('Doctorant', 'Doctorant'),('NULL','NULL')])
    grade_recherche=models.CharField(max_length=50 ,  choices=[('Directeur de recherche','Directeur de recherche'),('Maître de recherche','Maître de recherche'),('NULL','NULL')])
    Qualite =models.CharField(max_length=50 ,choices=[('Enseignant-Chercheur', 'Enseignant-Chercheur'), ('Chercheur', 'Chercheur'), ('Doctorant', 'Doctorant'), ('Autre', 'Autre')])
    # photo=models.ImageField(upload_to='photos/')
    h_index=models.CharField(max_length=50)
    equipe=models.CharField(max_length=50)
    statut=models.CharField(max_length=50)
    class Meta:
        db_table = 'Chercheurs'

    def __str__(self):
        return f"{self.nom_chercheur} {self.prenom_chercheur}"



class Conf_journal(models.Model):
    acronyme=models.CharField(max_length=50, primary_key=True)
    nom=models.CharField(max_length=50 ,null=False)
    p_type=models.CharField(max_length=50,null=False, choices=[('Conférence', 'Conférence'), ('Journal', 'Journal')])
    periodicite=models.CharField(max_length=50, choices=[('Ad hoc', 'Ad hoc'), ('Continuelle', 'Continuelle'), ('Saisonnière', 'Saisonnière'), ('Mensuelle', 'Mensuelle'), ('Bimensuelle', 'Bimensuelle'), ('Trimestrielle', 'Trimestrielle'), ('Semestrielle', 'Semestrielle'), ('Annuelle', 'Annuelle'), ('Biennale', 'Biennale'), ('Triennale', 'Triennale'), ('Quadriennale', 'Quadriennale'), ('Quinquemestrielle', 'Quinquemestrielle'), ('Hebdomadaire', 'Hebdomadaire'), ('Biquadrimestrielle', 'Biquadrimestrielle'), ('Spéciale/Supplémentaire', 'Spéciale/Supplémentaire'), ('autre', 'autre')] )
    lien=models.CharField(max_length=50)
    core_classification=models.CharField(max_length=50,choices=[('A*', 'A*'), ('A', 'A'), ('B', 'B'), ('C', 'C')])
    scimago_classification=models.CharField(max_length=50, choices=[('Q1', 'Q1'), ('Q2', 'Q2'), ('Q3', 'Q3'), ('Q4', 'Q4')])
    qualis_classification=models.CharField(max_length=50 , choices=[('A1', 'A1'), ('A2', 'A2'), ('B1', 'B1'), ('B2', 'B2'), ('B3', 'B3'), ('B4', 'B4'), ('B5', 'B5'), ('C', 'C')])
    dgrsdt_classification=models.CharField(max_length=50,choices=[('A', 'A'), ('B', 'B'), ('Autre', 'Autre')])
    class Meta:  
        db_table = 'conf_journal'



#class Publication(models.Model):
#   id_publication=models.AutoField(primary_key=True)
#    p_date=models.DateField()
#    id_chercheur=models.CharField(max_length=50 ,default=0 ) # this default becouse i dont want to change the bdd right now
#    id_revue_conf=models.CharField(max_length=50 ,default=0 ) # this default becouse i dont want to change the bdd right now
#    titre_publication=models.CharField(max_length=50)
#    volume=models.CharField(max_length=50)
#    domaine=models.CharField(max_length=50)
#    citations=models.IntegerField()
#    lien_publie=models.CharField(max_length=50)
#    prolongement_page=models.CharField(max_length=50)
#    rang_chercheur=models.IntegerField()
    #id_revue_conf = models.ForeignKey(RevueConf ,on_delete=models.CASCADE,null=False,db_column='id_revue_conf')
#    class Meta:
#        db_table = 'publications'






    


class Encadrement (models.Model) : 
    id_encadrement=models.AutoField(primary_key=True)
    #id_chercheur = models.ForeignKey(Chercheur, on_delete=models.CASCADE, null=False,db_column='id_chercheur', default=None)
    type_encadrement=models.CharField(max_length=50 , choices=[('PFE', 'PFE'), ('Master', 'Master'), ('Doctorat', 'Doctorat'), ('Autre', 'Autre')])
    intitule=models.CharField(max_length=50, default=None)
    role_chercheur = models.CharField(max_length=50, choices=[('encadreur', 'Encadreur'), ('co_encadreur', 'Co_encadreur')], default='')
    annee_debut=models.IntegerField(db_column='année_debut')
    annee_fin=models.IntegerField(db_column='année_fin')
    nom_prenom_etd1=models.CharField(max_length=50)    
    nom_prenom_etd2=models.CharField(max_length=50)
    
    class Meta:
        # Define the composite primary key using unique_together
       # unique_together = ('id_chercheur', 'id_etudiant')
       db_table = 'encadrements'




        

#class Chercheurs_Projets(models.Model):
#    id_chercheurs_projets=models.AutoField(primary_key=True)
#    id_chercheur = models.ForeignKey(Chercheur, on_delete=models.CASCADE)
#    id_projet = models.ForeignKey(Projet, on_delete=models.CASCADE)

#class Chercheurs_Encadrements(models.Model):
#    id_chercheurs_encadrements=models.AutoField(primary_key=True)
#    id_chercheur = models.ForeignKey(Chercheur, on_delete=models.CASCADE)
#    id_encadrement = models.ForeignKey(Encadrement, on_delete=models.CASCADE)







# Create your models here.
