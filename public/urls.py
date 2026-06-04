from django.urls import path
from . import views
from . import api_views

app_name = 'public'

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('parametres/', views.parametres, name='parametres'),
    path('provinces/', views.list_provinces, name='list_provinces'),
    path('villes/', views.list_villes, name='list_villes'),
    path('centres/', views.list_centres, name='list_centres'),
    path('filieres/', views.list_filieres, name='list_filieres'),
    path('modules/', views.list_modules, name='list_modules'),
    path('niveaux/', views.list_niveaux, name='list_niveaux'),
    path('professeurs/', views.list_professeurs, name='list_professeurs'),
    path('articles/<int:article_id>/', views.detail_article, name='detail_article'),
    # Gestion des provinces (CRUD)
    path('provinces/create/', views.create_province, name='create_province'),
    path('provinces/<int:province_id>/edit/', views.edit_province, name='edit_province'),
    path('provinces/<int:province_id>/delete/', views.delete_province, name='delete_province'),
    # Gestion des villes (CRUD)
    path('villes/create/', views.create_ville, name='create_ville'),
    path('villes/<int:ville_id>/edit/', views.edit_ville, name='edit_ville'),
    path('villes/<int:ville_id>/delete/', views.delete_ville, name='delete_ville'),
    # Gestion des centres (CRUD)
    path('centres/create/', views.create_centre, name='create_centre'),
    path('centres/<int:centre_id>/edit/', views.edit_centre, name='edit_centre'),
    path('centres/<int:centre_id>/delete/', views.delete_centre, name='delete_centre'),
    # Gestion des filières par centre
    path('centres/<int:centre_id>/filieres/', views.list_filieres_by_centre, name='list_filieres_by_centre'),
    path('centres/<int:centre_id>/filieres/create/', views.create_filiere, name='create_filiere'),
    path('filieres/create/', views.create_filiere_generic, name='create_filiere_generic'),
    path('filieres/<int:filiere_id>/edit/', views.edit_filiere, name='edit_filiere'),
    path('filieres/<int:filiere_id>/delete/', views.delete_filiere, name='delete_filiere'),
    # Gestion des niveaux par filière
    path('filieres/<int:filiere_id>/niveaux/', views.list_niveaux_by_filiere, name='list_niveaux_by_filiere'),
    path('filieres/<int:filiere_id>/niveaux/create/', views.create_niveau, name='create_niveau'),
    path('niveaux/create/', views.create_niveau_generic, name='create_niveau_generic'),
    path('niveaux/<int:niveau_id>/edit/', views.edit_niveau, name='edit_niveau'),
    path('niveaux/<int:niveau_id>/delete/', views.delete_niveau, name='delete_niveau'),
    # Gestion des modules par niveau
    path('niveaux/<int:niveau_id>/modules/', views.list_modules_by_niveau, name='list_modules_by_niveau'),
    path('niveaux/<int:niveau_id>/modules/create/', views.create_module, name='create_module'),
    path('modules/create/', views.create_module_generic, name='create_module_generic'),
    path('modules/<int:module_id>/edit/', views.edit_module, name='edit_module'),
    path('modules/<int:module_id>/delete/', views.delete_module, name='delete_module'),
    # Professeurs assignés à un module
    path('modules/<int:module_id>/professeurs/', views.list_professeurs_by_module, name='list_professeurs_by_module'),
    # Liste globale des supports de cours
    path('supports/', views.list_supports_cours, name='list_supports_cours'),
    # Création générique de support (selection du module d'abord)
    path('supports/create/', views.create_support, name='create_support'),
    # Gestion des supports de cours par module
    path('modules/<int:module_id>/supports/', views.list_supports_by_module, name='list_supports_by_module'),
    path('modules/<int:module_id>/supports/create/', views.create_support, name='create_support_by_module'),
    path('supports/<int:support_id>/edit/', views.edit_support, name='edit_support'),
    path('supports/<int:support_id>/delete/', views.delete_support, name='delete_support'),
    # Gestion des étudiants par niveau
    path('niveaux/<int:niveau_id>/etudiants/', views.list_etudiants_by_niveau, name='list_etudiants_by_niveau'),
    path('niveaux/<int:niveau_id>/etudiants/create/', views.create_etudiant, name='create_etudiant'),
    path('etudiants/<int:etudiant_id>/edit/', views.edit_etudiant, name='edit_etudiant'),
    path('etudiants/<int:etudiant_id>/delete/', views.delete_etudiant, name='delete_etudiant'),
    # Gestion des professeurs (CRUD)
    path('professeurs/create/', views.create_professeur, name='create_professeur'),
    path('professeurs/<int:professeur_id>/modules/', views.list_modules_by_professeur, name='list_modules_by_professeur'),
    path('professeurs/<int:professeur_id>/edit/', views.edit_professeur, name='edit_professeur'),
    path('professeurs/<int:professeur_id>/delete/', views.delete_professeur, name='delete_professeur'),
    # Gestion des statuts étudiants
    path('statuts/', views.list_statuts, name='list_statuts'),
    path('statuts/create/', views.create_statut, name='create_statut'),
    path('statuts/<int:statut_id>/edit/', views.edit_statut, name='edit_statut'),
    path('statuts/<int:statut_id>/delete/', views.delete_statut, name='delete_statut'),
    # Gestion des articles
    path('articles/', views.list_articles, name='list_articles'),
    path('articles/create/', views.create_article, name='create_article'),
    path('articles/<int:article_id>/edit/', views.edit_article, name='edit_article'),
    path('articles/<int:article_id>/delete/', views.delete_article, name='delete_article'),
    # Gestion des messages de contact
    path('messages/', views.list_messages_contact, name='list_messages_contact'),
    path('administrateurs/', views.list_administrateurs, name='list_administrateurs'),
    path('administrateurs/create/', views.create_administrateur, name='create_administrateur'),
    path('administrateurs/<int:admin_id>/edit/', views.edit_administrateur, name='edit_administrateur'),
    path('administrateurs/<int:admin_id>/delete/', views.delete_administrateur, name='delete_administrateur'),
    # Paramètres
    path('parametres/', views.parametres, name='parametres'),
    path('mon-profil/', views.mon_profil, name='mon_profil'),
    path('parametres-sous-admin/', views.parametres, name='parametres_sous_admin'),
    # API endpoints
    path('api/provinces/', api_views.api_provinces, name='api_provinces'),
    path('api/villes/<int:province_id>/', api_views.api_villes, name='api_villes'),
    path('api/centres/<int:province_id>/', api_views.api_centres, name='api_centres'),
]
