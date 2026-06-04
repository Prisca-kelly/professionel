from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser, User

class Province(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name = "Province"
        verbose_name_plural = "Provinces"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom

class Ville(models.Model):
    nom = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='villes')
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Ville"
        verbose_name_plural = "Villes"
        ordering = ['nom']
    
    def __str__(self):
        return f"{self.nom} ({self.province.nom})"

class Centre(models.Model):
    nom = models.CharField(max_length=200)
    adresse = models.TextField(blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    type_centre = models.CharField(max_length=100, default="Centre de formation")
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE, related_name='centres')
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Centre de formation"
        verbose_name_plural = "Centres de formation"
        ordering = ['nom']
    
    def __str__(self):
        return f"{self.nom} ({self.ville.nom})"

class Article(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    fichier = models.FileField(upload_to='articles/', null=True, blank=True, help_text="Fichier joint à l'article (PDF, DOC, etc.)")
    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)
    publie = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['-date_creation']
    
    def __str__(self):
        return self.titre

class MessageContact(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    sujet = models.CharField(max_length=200)
    message = models.TextField()
    date_envoi = models.DateTimeField(default=timezone.now)
    traite = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ['-date_envoi']
    
    def __str__(self):
        return f"{self.nom} - {self.sujet}"


class AdminProfile(models.Model):
    ROLE_CHOICES = [
        ('ADMIN-PRINCIPAL', 'Administrateur Principal'),
        ('SOUS-ADMIN', 'Sous-Administrateur'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='SOUS-ADMIN')
    centre = models.ForeignKey(Centre, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='administrateurs',
                                help_text="Centre assigné au sous-admin (non utilisé pour admin principal)")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Profil Administrateur"
        verbose_name_plural = "Profils Administrateurs"
        ordering = ['user__username']

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    def is_admin_principal(self):
        return self.role == 'ADMIN-PRINCIPAL'

    def is_sous_admin(self):
        return self.role == 'SOUS-ADMIN'


class Filiere(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    centre = models.ForeignKey(Centre, on_delete=models.CASCADE, related_name='filieres')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Filière"
        verbose_name_plural = "Filières"
        ordering = ['nom']

    def __str__(self):
        return f"{self.nom} - {self.centre.nom}"


class Niveau(models.Model):
    nom = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name='niveaux')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Niveau"
        verbose_name_plural = "Niveaux"
        ordering = ['nom']

    def __str__(self):
        return f"{self.nom} - {self.filiere.nom}"


class Professeur(models.Model):
    nom = models.CharField(max_length=120)
    prenom = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    telephone = models.CharField(max_length=40, blank=True)
    centre = models.ForeignKey(Centre, on_delete=models.CASCADE, related_name='professeurs')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Professeur"
        verbose_name_plural = "Professeurs"
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Module(models.Model):
    code = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, related_name='modules')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Module"
        verbose_name_plural = "Modules"
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.nom}"


class ModuleProfesseur(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='professeurs_assignes')
    professeur = models.ForeignKey(Professeur, on_delete=models.CASCADE, related_name='modules_assignes')
    annee_academique = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Assignation Module-Professeur"
        verbose_name_plural = "Assignations Module-Professeur"
        unique_together = ['module', 'professeur', 'annee_academique']

    def __str__(self):
        return f"{self.professeur} - {self.module} ({self.annee_academique})"


class SupportCours(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    fichier_url = models.CharField(max_length=255, blank=True, default='')
    fichier = models.FileField(
        upload_to='supports/%Y/%m/',
        max_length=500,
        blank=True,
        null=True,
        help_text='Fichier uploadé (prioritaire sur l’URL si les deux sont renseignés).',
    )
    type_fichier = models.CharField(max_length=40, blank=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='supports')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Support de cours"
        verbose_name_plural = "Supports de cours"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.titre} - {self.module.nom}"

    @property
    def lien_telechargement(self):
        if self.fichier:
            return self.fichier.url
        url = (self.fichier_url or '').strip()
        if not url:
            return ''
        if url.startswith(('http://', 'https://')):
            return url
        if not url.startswith('/'):
            url = '/' + url
        return url


class StatutEtudiant(models.Model):
    libelle = models.CharField(max_length=60, unique=True)

    class Meta:
        verbose_name = "Statut Étudiant"
        verbose_name_plural = "Statuts Étudiants"
        ordering = ['libelle']

    def __str__(self):
        return self.libelle


class Etudiant(models.Model):
    matricule = models.CharField(max_length=40, unique=True)
    nom = models.CharField(max_length=120)
    prenom = models.CharField(max_length=120)
    SEXE_CHOICES = [('M', 'Masculin'), ('F', 'Féminin')]
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    date_naissance = models.DateField(null=True, blank=True)
    telephone = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    adresse = models.TextField(blank=True)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, related_name='etudiants')
    statut = models.ForeignKey(StatutEtudiant, on_delete=models.CASCADE, related_name='etudiants')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Étudiant"
        verbose_name_plural = "Étudiants"
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.matricule})"
