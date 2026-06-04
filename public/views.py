from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Count
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Article, AdminProfile, Province, Ville, Centre, Filiere, Niveau, Professeur, Module, ModuleProfesseur, SupportCours, StatutEtudiant, Etudiant, MessageContact

# ==================== HELPER FUNCTIONS FOR SOUS-ADMIN ACCESS CONTROL ====================

def get_user_centre(request):
    """Récupère le centre de l'utilisateur s'il est un sous-admin, None sinon."""
    if not request.user.is_authenticated:
        return None
    
    try:
        admin_profile = AdminProfile.objects.get(user=request.user)
        if admin_profile.is_sous_admin():
            return admin_profile.centre
    except AdminProfile.DoesNotExist:
        pass
    
    return None


def check_centre_access(request, centre_id):
    """Vérifie si un sous-admin a accès à un centre donné."""
    user_centre = get_user_centre(request)
    if user_centre is None:
        # Admin principal - accès complet
        return True
    
    # Sous-admin - vérifier l'accès au centre
    return int(centre_id) == user_centre.id


def check_resource_centre_access(request, resource_object, centre_field='centre'):
    """Vérifie si un sous-admin a accès à une ressource basée sur son centre."""
    user_centre = get_user_centre(request)
    if user_centre is None:
        # Admin principal - accès complet
        return True
    
    # Récupérer le centre de la ressource
    resource_centre = resource_object
    for field in centre_field.split('__'):
        resource_centre = getattr(resource_centre, field)
    
    # Vérifier l'accès
    return resource_centre.id == user_centre.id


def accueil(request):
    articles_publies = Article.objects.filter(publie=True)
    return render(request, 'public/accueil.html', {
        'articles': articles_publies
    })

@csrf_exempt
@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('public:dashboard')
    
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_staff:
                login(request, user)
                next_url = request.POST.get('next') or 'public:dashboard'
                return redirect(next_url)
            else:
                error = 'Vous n\'avez pas accès à l\'administration.'
        else:
            error = 'Identifiants invalides. Veuillez réessayer.'
    
    return render(request, 'public/login.html', {'error': error})

def logout_view(request):
    logout(request)
    return redirect('public:login')

@login_required(login_url='public:login')
def dashboard(request):
    if not request.user.is_staff:
        return redirect('public:accueil')
    
    # Récupérer ou créer le profil admin
    admin_profile, created = AdminProfile.objects.get_or_create(
        user=request.user,
        defaults={'role': 'ADMIN-PRINCIPAL'}
    )
    
    # Déterminer le type de dashboard selon le rôle
    is_admin_principal = admin_profile.is_admin_principal()
    
    # Récupérer le centre pour les sous-admins
    user_centre = get_user_centre(request)
    
    # Récupérer les statistiques
    if is_admin_principal:
        total_provinces = Province.objects.count()
        total_villes = Ville.objects.count()
        total_centres = Centre.objects.count()
        total_filieres = Filiere.objects.count()
        total_niveaux = Niveau.objects.count()
        total_professeurs = Professeur.objects.count()
        total_modules = Module.objects.count()
        total_etudiants = Etudiant.objects.count()
        total_articles = Article.objects.count()
        total_articles_publies = Article.objects.filter(publie=True).count()
        total_supports = SupportCours.objects.count()
        total_messages = MessageContact.objects.count()
    else:
        # Pour les sous-admins, filtrer par centre
        total_provinces = 0
        total_villes = 0
        total_centres = 1  # Leur centre
        total_filieres = Filiere.objects.filter(centre=user_centre).count()
        total_niveaux = Niveau.objects.filter(filiere__centre=user_centre).count()
        total_professeurs = Professeur.objects.filter(centre=user_centre).count()
        total_modules = Module.objects.filter(niveau__filiere__centre=user_centre).count()
        total_etudiants = Etudiant.objects.filter(niveau__filiere__centre=user_centre).count()
        total_articles = 0
        total_articles_publies = 0
        total_supports = SupportCours.objects.filter(module__niveau__filiere__centre=user_centre).count()
        total_messages = MessageContact.objects.count()
    
    context = {
        'user': request.user,
        'admin_profile': admin_profile,
        'is_admin_principal': is_admin_principal,
        # Statistiques
        'total_provinces': total_provinces,
        'total_villes': total_villes,
        'total_centres': total_centres,
        'total_filieres': total_filieres,
        'total_niveaux': total_niveaux,
        'total_professeurs': total_professeurs,
        'total_modules': total_modules,
        'total_etudiants': total_etudiants,
        'total_articles': total_articles,
        'total_articles_publies': total_articles_publies,
        'total_supports': total_supports,
        'total_messages': total_messages,
    }
    
    if is_admin_principal:
        return render(request, 'public/dashboard_admin_principal.html', context)
    else:
        return render(request, 'public/dashboard_sous_admin.html', context)

@login_required(login_url='public:login')
def parametres(request):
    if not request.user.is_staff:
        return redirect('public:accueil')
    
    # Récupérer le profil admin
    try:
        admin_profile = AdminProfile.objects.get(user=request.user)
    except AdminProfile.DoesNotExist:
        admin_profile = None
    
    # Déterminer le type de dashboard selon le rôle
    is_admin_principal = admin_profile and admin_profile.is_admin_principal()
    
    # Gestion du profil utilisateur
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_profile':
            request.user.first_name = request.POST.get('first_name', request.user.first_name)
            request.user.last_name = request.POST.get('last_name', request.user.last_name)
            request.user.email = request.POST.get('email', request.user.email)
            request.user.save()
            
            if admin_profile:
                admin_profile.telephone = request.POST.get('telephone', admin_profile.telephone)
                admin_profile.save()
        
        elif action == 'change_password':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            if request.user.check_password(old_password):
                if new_password == confirm_password:
                    request.user.set_password(new_password)
                    request.user.save()
                    from django.contrib.auth import update_session_auth_hash
                    update_session_auth_hash(request, request.user)
                else:
                    return render(request, 'public/parametres.html', {
                        'error': 'Les mots de passe ne correspondent pas',
                        'user': request.user,
                        'admin_profile': admin_profile,
                        'is_admin_principal': is_admin_principal,
                    })
            else:
                return render(request, 'public/parametres.html', {
                    'error': 'L\'ancien mot de passe est incorrect',
                    'user': request.user,
                    'admin_profile': admin_profile,
                    'is_admin_principal': is_admin_principal,
                })
    
    context = {
        'user': request.user,
        'admin_profile': admin_profile,
        'is_admin_principal': is_admin_principal,
    }
    
    return render(request, 'public/parametres.html', context)

@login_required(login_url='public:login')
def list_provinces(request):
    if not request.user.is_staff:
        return redirect('public:accueil')
    
    provinces = Province.objects.all()
    return render(request, 'public/list_provinces.html', {'provinces': provinces})

@login_required(login_url='public:login')
def list_villes(request):
    villes = Ville.objects.select_related('province').select_related('province').all()
    return render(request, 'public/list_villes.html', {'villes': villes})

@login_required(login_url='public:login')
def list_centres(request):
    centres = Centre.objects.select_related('ville__province').all()
    return render(request, 'public/list_centres.html', {'centres': centres})

@login_required(login_url='public:login')
def list_filieres(request):
    user_centre = get_user_centre(request)
    if user_centre is not None:
        # Sous-admin: filtrer par centre
        filieres = Filiere.objects.filter(centre=user_centre)
    else:
        # Admin principal: afficher tout
        filieres = Filiere.objects.all()
    
    return render(request, 'public/list_filieres.html', {'filieres': filieres})

@login_required(login_url='public:login')
def list_modules(request):
    user_centre = get_user_centre(request)
    if user_centre is not None:
        # Sous-admin: filtrer par centre
        modules = Module.objects.filter(niveau__filiere__centre=user_centre)
    else:
        # Admin principal: afficher tout
        modules = Module.objects.all()
    
    return render(request, 'public/list_modules.html', {'modules': modules})

@login_required(login_url='public:login')
def list_niveaux(request):
    user_centre = get_user_centre(request)
    if user_centre is not None:
        # Sous-admin: filtrer par centre
        niveaux = Niveau.objects.filter(filiere__centre=user_centre).select_related('filiere__centre')
    else:
        # Admin principal: afficher tout
        niveaux = Niveau.objects.select_related('filiere__centre').all()
    
    return render(request, 'public/list_niveaux.html', {'niveaux': niveaux})

@login_required(login_url='public:login')
def list_professeurs(request):
    user_centre = get_user_centre(request)
    if user_centre is not None:
        # Sous-admin: filtrer par centre
        professeurs = Professeur.objects.filter(centre=user_centre).annotate(
            nb_modules=Count('modules_assignes')
        )
    else:
        # Admin principal: afficher tout
        professeurs = Professeur.objects.select_related('centre').annotate(
            nb_modules=Count('modules_assignes')
        )
    
    return render(request, 'public/list_professeurs.html', {'professeurs': professeurs})


@login_required(login_url='public:login')
def list_modules_by_professeur(request, professeur_id):
    professeur = get_object_or_404(Professeur.objects.select_related('centre'), id=professeur_id)
    assignations = (
        professeur.modules_assignes
        .select_related(
            'module',
            'module__niveau',
            'module__niveau__filiere',
            'module__niveau__filiere__centre',
        )
        .order_by('-annee_academique', 'module__code')
    )
    return render(request, 'public/list_modules_by_professeur.html', {
        'professeur': professeur,
        'assignations': assignations,
    })

# ==================== GESTION DES PROVINCES ====================
@login_required(login_url='public:login')
def create_province(request):
    if request.method == 'POST':
        nom = request.POST.get('nom', '').strip()
        if nom:
            Province.objects.create(nom=nom)
            return redirect('public:list_provinces')

    return render(request, 'public/create_province.html')

@login_required(login_url='public:login')
def edit_province(request, province_id):
    province = get_object_or_404(Province, id=province_id)

    if request.method == 'POST':
        nom = request.POST.get('nom', '').strip()
        if nom:
            province.nom = nom
            province.save()
        return redirect('public:list_provinces')

    return render(request, 'public/edit_province.html', {'province': province})

@login_required(login_url='public:login')
def delete_province(request, province_id):
    province = get_object_or_404(Province, id=province_id)
    if request.method == 'POST':
        province.delete()
        return redirect('public:list_provinces')
    return render(request, 'public/delete_province.html', {'province': province})

# ==================== GESTION DES VILLES ====================
@login_required(login_url='public:login')
def create_ville(request):
    provinces = Province.objects.all()
    if request.method == 'POST':
        nom = request.POST.get('nom')
        province_id = request.POST.get('province')
        if nom and province_id:
            province = get_object_or_404(Province, id=province_id)
            Ville.objects.create(nom=nom, province=province)
            return redirect('public:list_villes')

    return render(request, 'public/create_ville.html', {'provinces': provinces})

@login_required(login_url='public:login')
def edit_ville(request, ville_id):
    ville = get_object_or_404(Ville, id=ville_id)
    provinces = Province.objects.all()

    if request.method == 'POST':
        ville.nom = request.POST.get('nom', ville.nom)
        province_id = request.POST.get('province')
        if province_id:
            ville.province = get_object_or_404(Province, id=province_id)
        ville.save()
        return redirect('public:list_villes')

    return render(request, 'public/edit_ville.html', {'ville': ville, 'provinces': provinces})

@login_required(login_url='public:login')
def delete_ville(request, ville_id):
    ville = get_object_or_404(Ville, id=ville_id)
    if request.method == 'POST':
        ville.delete()
        return redirect('public:list_villes')
    return render(request, 'public/delete_ville.html', {'ville': ville})

# ==================== GESTION DES PROFESSEURS ====================
@login_required(login_url='public:login')
def create_professeur(request):
    centres = Centre.objects.select_related('ville__province').all()
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        centre_id = request.POST.get('centre')

        if nom and prenom and centre_id:
            centre = get_object_or_404(Centre, id=centre_id)
            Professeur.objects.create(
                nom=nom,
                prenom=prenom,
                email=email,
                telephone=telephone,
                centre=centre
            )
            return redirect('public:list_professeurs')

    return render(request, 'public/create_professeur.html', {'centres': centres})

@login_required(login_url='public:login')
def edit_professeur(request, professeur_id):
    professeur = get_object_or_404(Professeur, id=professeur_id)
    centres = Centre.objects.select_related('ville__province').all()

    if request.method == 'POST':
        professeur.nom = request.POST.get('nom', professeur.nom)
        professeur.prenom = request.POST.get('prenom', professeur.prenom)
        professeur.email = request.POST.get('email', professeur.email)
        professeur.telephone = request.POST.get('telephone', professeur.telephone)
        centre_id = request.POST.get('centre')
        if centre_id:
            professeur.centre = get_object_or_404(Centre, id=centre_id)
        professeur.save()
        return redirect('public:list_professeurs')

    return render(request, 'public/edit_professeur.html', {'professeur': professeur, 'centres': centres})

@login_required(login_url='public:login')
def delete_professeur(request, professeur_id):
    professeur = get_object_or_404(Professeur, id=professeur_id)
    if request.method == 'POST':
        professeur.delete()
        return redirect('public:list_professeurs')
    return render(request, 'public/delete_professeur.html', {'professeur': professeur})

# ==================== GESTION DES CENTRES ====================
@login_required(login_url='public:login')
def create_centre(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        adresse = request.POST.get('adresse')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        type_centre = request.POST.get('type_centre', 'Centre de formation')
        ville_id = request.POST.get('ville')
        
        if nom and ville_id:
            from .models import Ville
            ville = get_object_or_404(Ville, id=ville_id)
            Centre.objects.create(
                nom=nom,
                adresse=adresse,
                telephone=telephone,
                email=email,
                type_centre=type_centre,
                ville=ville
            )
            return redirect('public:list_centres')
    
    from .models import Ville
    villes = Ville.objects.all()
    return render(request, 'public/create_centre.html', {'villes': villes})

@login_required(login_url='public:login')
def edit_centre(request, centre_id):
    centre = get_object_or_404(Centre, id=centre_id)
    
    if request.method == 'POST':
        centre.nom = request.POST.get('nom', centre.nom)
        centre.adresse = request.POST.get('adresse', centre.adresse)
        centre.telephone = request.POST.get('telephone', centre.telephone)
        centre.email = request.POST.get('email', centre.email)
        centre.type_centre = request.POST.get('type_centre', centre.type_centre)
        ville_id = request.POST.get('ville')
        
        if ville_id:
            from .models import Ville
            ville = get_object_or_404(Ville, id=ville_id)
            centre.ville = ville
        
        centre.save()
        return redirect('public:list_centres')
    
    from .models import Ville
    villes = Ville.objects.all()
    return render(request, 'public/edit_centre.html', {'centre': centre, 'villes': villes})

@login_required(login_url='public:login')
def delete_centre(request, centre_id):
    centre = get_object_or_404(Centre, id=centre_id)
    
    if request.method == 'POST':
        centre.delete()
        return redirect('public:list_centres')
    
    return render(request, 'public/delete_centre.html', {'centre': centre})

# ==================== GESTION DES FILIÈRES ====================
@login_required(login_url='public:login')
def list_filieres_by_centre(request, centre_id):
    centre = get_object_or_404(Centre, id=centre_id)
    filieres = centre.filieres.all()
    return render(request, 'public/list_filieres_by_centre.html', {'centre': centre, 'filieres': filieres})

@login_required(login_url='public:login')
def create_filiere(request, centre_id):
    centre = get_object_or_404(Centre, id=centre_id)
    
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        
        if nom:
            Filiere.objects.create(
                nom=nom,
                description=description,
                centre=centre
            )
            return redirect('public:list_filieres_by_centre', centre_id=centre.id)
    
    return render(request, 'public/create_filiere.html', {'centre': centre})

@login_required(login_url='public:login')
def edit_filiere(request, filiere_id):
    filiere = get_object_or_404(Filiere, id=filiere_id)
    
    if request.method == 'POST':
        filiere.nom = request.POST.get('nom', filiere.nom)
        filiere.description = request.POST.get('description', filiere.description)
        filiere.save()
        return redirect('public:list_filieres_by_centre', centre_id=filiere.centre.id)
    
    return render(request, 'public/edit_filiere.html', {'filiere': filiere})

@login_required(login_url='public:login')
def delete_filiere(request, filiere_id):
    filiere = get_object_or_404(Filiere, id=filiere_id)
    centre_id = filiere.centre.id
    
    if request.method == 'POST':
        filiere.delete()
        return redirect('public:list_filieres_by_centre', centre_id=centre_id)
    
    return render(request, 'public/delete_filiere.html', {'filiere': filiere})

# ==================== GESTION DES NIVEAUX ====================
@login_required(login_url='public:login')
def list_niveaux_by_filiere(request, filiere_id):
    filiere = get_object_or_404(Filiere, id=filiere_id)
    niveaux = filiere.niveaux.all()
    return render(request, 'public/list_niveaux_by_filiere.html', {'filiere': filiere, 'niveaux': niveaux})

@login_required(login_url='public:login')
def create_niveau(request, filiere_id):
    filiere = get_object_or_404(Filiere, id=filiere_id)
    
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        
        if nom:
            Niveau.objects.create(
                nom=nom,
                description=description,
                filiere=filiere
            )
            return redirect('public:list_niveaux_by_filiere', filiere_id=filiere.id)
    
    return render(request, 'public/create_niveau.html', {'filiere': filiere})

@login_required(login_url='public:login')
def edit_niveau(request, niveau_id):
    niveau = get_object_or_404(Niveau, id=niveau_id)
    
    if request.method == 'POST':
        niveau.nom = request.POST.get('nom', niveau.nom)
        niveau.description = request.POST.get('description', niveau.description)
        niveau.save()
        return redirect('public:list_niveaux_by_filiere', filiere_id=niveau.filiere.id)
    
    return render(request, 'public/edit_niveau.html', {'niveau': niveau})

@login_required(login_url='public:login')
def delete_niveau(request, niveau_id):
    niveau = get_object_or_404(Niveau, id=niveau_id)
    filiere_id = niveau.filiere.id
    
    if request.method == 'POST':
        niveau.delete()
        return redirect('public:list_niveaux_by_filiere', filiere_id=filiere_id)
    
    return render(request, 'public/delete_niveau.html', {'niveau': niveau})

# ==================== GESTION DES MODULES ====================
@login_required(login_url='public:login')
def list_modules_by_niveau(request, niveau_id):
    niveau = get_object_or_404(Niveau, id=niveau_id)
    modules = niveau.modules.all()
    return render(request, 'public/list_modules_by_niveau.html', {'niveau': niveau, 'modules': modules})

@login_required(login_url='public:login')
def create_module(request, niveau_id):
    niveau = get_object_or_404(Niveau, id=niveau_id)
    
    if request.method == 'POST':
        code = request.POST.get('code')
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        
        if code and nom:
            Module.objects.create(
                code=code,
                nom=nom,
                description=description,
                niveau=niveau
            )
            return redirect('public:list_modules_by_niveau', niveau_id=niveau.id)
    
    return render(request, 'public/create_module.html', {'niveau': niveau})

@login_required(login_url='public:login')
def edit_module(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    
    if request.method == 'POST':
        module.code = request.POST.get('code', module.code)
        module.nom = request.POST.get('nom', module.nom)
        module.description = request.POST.get('description', module.description)
        module.save()
        return redirect('public:list_modules_by_niveau', niveau_id=module.niveau.id)
    
    return render(request, 'public/edit_module.html', {'module': module})

@login_required(login_url='public:login')
def delete_module(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    niveau_id = module.niveau.id
    
    if request.method == 'POST':
        module.delete()
        return redirect('public:list_modules_by_niveau', niveau_id=niveau_id)
    
    return render(request, 'public/delete_module.html', {'module': module})

# ==================== PROFESSEURS PAR MODULE ====================
def _redirect_professeurs_module(request, module_id):
    url = reverse('public:list_professeurs_by_module', kwargs={'module_id': module_id})
    back = request.POST.get('back') or request.GET.get('back')
    if back == 'list_modules':
        url += '?back=list_modules'
    return redirect(url)


@login_required(login_url='public:login')
def list_professeurs_by_module(request, module_id):
    module = get_object_or_404(
        Module.objects.select_related('niveau__filiere__centre'),
        id=module_id,
    )
    centre = module.niveau.filiere.centre
    back_param = request.GET.get('back', '')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'assign':
            professeur_id = request.POST.get('professeur')
            annee_academique = request.POST.get('annee_academique', '').strip()
            if professeur_id and annee_academique:
                professeur = get_object_or_404(Professeur, id=professeur_id, centre=centre)
                try:
                    ModuleProfesseur.objects.create(
                        module=module,
                        professeur=professeur,
                        annee_academique=annee_academique,
                    )
                    messages.success(
                        request,
                        f'{professeur} a été assigné au module pour {annee_academique}.',
                    )
                except IntegrityError:
                    messages.error(
                        request,
                        'Cette assignation existe déjà pour cette année académique.',
                    )
            else:
                messages.error(request, 'Veuillez sélectionner un professeur et une année académique.')

        elif action == 'unassign':
            assignation_id = request.POST.get('assignation_id')
            assignation = get_object_or_404(
                ModuleProfesseur,
                id=assignation_id,
                module=module,
            )
            professeur_nom = str(assignation.professeur)
            assignation.delete()
            messages.success(request, f'{professeur_nom} a été retiré du module.')

        return _redirect_professeurs_module(request, module_id)

    assignations = (
        module.professeurs_assignes
        .select_related('professeur', 'professeur__centre')
        .order_by('-annee_academique', 'professeur__nom', 'professeur__prenom')
    )
    professeurs = Professeur.objects.filter(centre=centre).order_by('nom', 'prenom')

    if back_param == 'list_modules':
        back_url = reverse('public:list_modules')
        back_label = 'Retour à la liste des modules'
    else:
        back_url = reverse('public:list_modules_by_niveau', kwargs={'niveau_id': module.niveau.id})
        back_label = 'Retour aux modules'

    year = date.today().year
    default_annee = f'{year}-{year + 1}'

    return render(request, 'public/list_professeurs_by_module.html', {
        'module': module,
        'assignations': assignations,
        'professeurs': professeurs,
        'centre': centre,
        'back_url': back_url,
        'back_label': back_label,
        'back_param': back_param,
        'default_annee': default_annee,
    })

# ==================== GESTION DES SUPPORTS DE COURS ====================
@login_required(login_url='public:login')
def list_supports_cours(request):
    if not request.user.is_staff:
        return redirect('public:accueil')
    supports = SupportCours.objects.select_related(
        'module',
        'module__niveau',
        'module__niveau__filiere',
        'module__niveau__filiere__centre',
        'uploaded_by',
    ).order_by('-created_at')
    try:
        admin_profile = AdminProfile.objects.get(user=request.user)
    except AdminProfile.DoesNotExist:
        admin_profile = None
    if admin_profile and admin_profile.is_sous_admin() and admin_profile.centre_id:
        supports = supports.filter(module__niveau__filiere__centre_id=admin_profile.centre_id)
    return render(request, 'public/list_supports_cours.html', {'supports': supports})


@login_required(login_url='public:login')
def list_supports_by_module(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    supports = module.supports.all()
    return render(request, 'public/list_supports_by_module.html', {'module': module, 'supports': supports})

@login_required(login_url='public:login')
def create_support(request, module_id=None):
    """Création de support de cours avec sélection optionnelle du module"""
    
    # Si module_id n'est pas fourni, demander à l'utilisateur de le choisir
    if module_id is None:
        modules = Module.objects.select_related('niveau__filiere__centre').all()
        
        if request.method == 'POST':
            module_id = request.POST.get('module')
            if module_id:
                return redirect('public:create_support', module_id=module_id)
            else:
                messages.error(request, 'Veuillez sélectionner un module.')
        
        return render(request, 'public/create_support_generic.html', {'modules': modules})
    
    # Si module_id est fourni, créer le support
    module = get_object_or_404(Module, id=module_id)

    if request.method == 'POST':
        titre = (request.POST.get('titre') or '').strip()
        description = request.POST.get('description', '')
        fichier_url = (request.POST.get('fichier_url') or '').strip()
        type_fichier = (request.POST.get('type_fichier') or '').strip()
        uploaded = request.FILES.get('fichier')

        if not titre:
            messages.error(request, 'Le titre est obligatoire.')
        elif not uploaded and not fichier_url:
            messages.error(request, 'Veuillez joindre un fichier ou indiquer une URL.')
        else:
            if uploaded and not type_fichier:
                name = uploaded.name
                type_fichier = name.rsplit('.', 1)[-1].upper() if '.' in name else ''

            SupportCours.objects.create(
                titre=titre,
                description=description,
                fichier_url=fichier_url if not uploaded else '',
                fichier=uploaded if uploaded else None,
                type_fichier=type_fichier,
                module=module,
                uploaded_by=request.user,
            )
            return redirect('public:list_supports_by_module', module_id=module.id)

    return render(request, 'public/create_support.html', {'module': module})


@login_required(login_url='public:login')
def edit_support(request, support_id):
    support = get_object_or_404(SupportCours, id=support_id)

    if request.method == 'POST':
        titre = (request.POST.get('titre') or '').strip()
        fichier_url = (request.POST.get('fichier_url') or '').strip()
        type_fichier = (request.POST.get('type_fichier') or '').strip()
        uploaded = request.FILES.get('fichier')

        if not titre:
            messages.error(request, 'Le titre est obligatoire.')
        elif not uploaded and not fichier_url and not support.fichier:
            messages.error(request, 'Veuillez joindre un fichier ou indiquer une URL.')
        else:
            support.titre = titre
            support.description = request.POST.get('description', support.description)
            if uploaded:
                if support.fichier:
                    support.fichier.delete(save=False)
                support.fichier = uploaded
                support.fichier_url = ''
                if not type_fichier:
                    name = uploaded.name
                    type_fichier = name.rsplit('.', 1)[-1].upper() if '.' in name else ''
            else:
                support.fichier_url = fichier_url
            support.type_fichier = type_fichier
            support.save()
            messages.success(request, 'Support de cours modifié avec succès!')
            return redirect('public:list_supports_cours')

    return render(request, 'public/edit_support.html', {'support': support})


@login_required(login_url='public:login')
def delete_support(request, support_id):
    support = get_object_or_404(SupportCours, id=support_id)

    if request.method == 'POST':
        if support.fichier:
            support.fichier.delete(save=False)
        support.delete()
        messages.success(request, 'Support de cours supprimé avec succès!')
        return redirect('public:list_supports_cours')

    return render(request, 'public/delete_support.html', {'support': support})

# ==================== GESTION DES ÉTUDIANTS ====================
@login_required(login_url='public:login')
def list_etudiants_by_niveau(request, niveau_id):
    niveau = get_object_or_404(Niveau, id=niveau_id)
    etudiants = niveau.etudiants.all()
    return render(request, 'public/list_etudiants_by_niveau.html', {'niveau': niveau, 'etudiants': etudiants})

@login_required(login_url='public:login')
def create_etudiant(request, niveau_id):
    niveau = get_object_or_404(Niveau, id=niveau_id)
    statuts = StatutEtudiant.objects.all()
    
    if request.method == 'POST':
        matricule = request.POST.get('matricule')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        sexe = request.POST.get('sexe')
        date_naissance = request.POST.get('date_naissance')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        adresse = request.POST.get('adresse')
        statut_id = request.POST.get('statut')
        
        if matricule and nom and prenom and statut_id:
            from datetime import datetime
            date_naissance_obj = None
            if date_naissance:
                date_naissance_obj = datetime.strptime(date_naissance, '%Y-%m-%d').date()
            
            statut = get_object_or_404(StatutEtudiant, id=statut_id)
            Etudiant.objects.create(
                matricule=matricule,
                nom=nom,
                prenom=prenom,
                sexe=sexe,
                date_naissance=date_naissance_obj,
                telephone=telephone,
                email=email,
                adresse=adresse,
                niveau=niveau,
                statut=statut
            )
            return redirect('public:list_etudiants_by_niveau', niveau_id=niveau.id)
    
    return render(request, 'public/create_etudiant.html', {'niveau': niveau, 'statuts': statuts})

@login_required(login_url='public:login')
def edit_etudiant(request, etudiant_id):
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)
    statuts = StatutEtudiant.objects.all()
    
    if request.method == 'POST':
        etudiant.matricule = request.POST.get('matricule', etudiant.matricule)
        etudiant.nom = request.POST.get('nom', etudiant.nom)
        etudiant.prenom = request.POST.get('prenom', etudiant.prenom)
        etudiant.sexe = request.POST.get('sexe', etudiant.sexe)
        date_naissance = request.POST.get('date_naissance')
        if date_naissance:
            from datetime import datetime
            etudiant.date_naissance = datetime.strptime(date_naissance, '%Y-%m-%d').date()
        etudiant.telephone = request.POST.get('telephone', etudiant.telephone)
        etudiant.email = request.POST.get('email', etudiant.email)
        etudiant.adresse = request.POST.get('adresse', etudiant.adresse)
        statut_id = request.POST.get('statut')
        if statut_id:
            etudiant.statut = get_object_or_404(StatutEtudiant, id=statut_id)
        etudiant.save()
        return redirect('public:list_etudiants_by_niveau', niveau_id=etudiant.niveau.id)
    
    return render(request, 'public/edit_etudiant.html', {'etudiant': etudiant, 'statuts': statuts})

@login_required(login_url='public:login')
def delete_etudiant(request, etudiant_id):
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)
    niveau_id = etudiant.niveau.id
    
    if request.method == 'POST':
        etudiant.delete()
        return redirect('public:list_etudiants_by_niveau', niveau_id=niveau_id)
    
    return render(request, 'public/delete_etudiant.html', {'etudiant': etudiant})

# ==================== GESTION DES STATUTS ÉTUDIANTS ====================
@login_required(login_url='public:login')
def list_statuts(request):
    statuts = StatutEtudiant.objects.all()
    return render(request, 'public/list_statuts.html', {'statuts': statuts})

@login_required(login_url='public:login')
def create_statut(request):
    if request.method == 'POST':
        libelle = request.POST.get('libelle')
        if libelle:
            StatutEtudiant.objects.create(libelle=libelle)
            return redirect('public:list_statuts')
    
    return render(request, 'public/create_statut.html')

@login_required(login_url='public:login')
def edit_statut(request, statut_id):
    statut = get_object_or_404(StatutEtudiant, id=statut_id)
    
    if request.method == 'POST':
        statut.libelle = request.POST.get('libelle', statut.libelle)
        statut.save()
        return redirect('public:list_statuts')
    
    return render(request, 'public/edit_statut.html', {'statut': statut})

@login_required(login_url='public:login')
def delete_statut(request, statut_id):
    statut = get_object_or_404(StatutEtudiant, id=statut_id)
    
    if request.method == 'POST':
        statut.delete()
        return redirect('public:list_statuts')
    
    return render(request, 'public/delete_statut.html', {'statut': statut})

# ==================== GESTION DES ARTICLES ====================
@login_required(login_url='public:login')
def list_articles(request):
    articles = Article.objects.all()
    articles_count = Article.objects.count()
    articles_published = Article.objects.filter(publie=True).count()
    articles_draft = Article.objects.filter(publie=False).count()
    
    context = {
        'articles': articles,
        'articles_count': articles_count,
        'articles_published': articles_published,
        'articles_draft': articles_draft,
    }
    return render(request, 'public/list_articles.html', context)

@login_required(login_url='public:login')
def create_article(request):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        contenu = request.POST.get('contenu')
        publie = request.POST.get('publie') == 'on'
        
        if titre and contenu:
            Article.objects.create(
                titre=titre,
                contenu=contenu,
                publie=publie
            )
            return redirect('public:list_articles')
    
    return render(request, 'public/create_article.html')

@login_required(login_url='public:login')
def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    
    if request.method == 'POST':
        article.titre = request.POST.get('titre', article.titre)
        article.contenu = request.POST.get('contenu', article.contenu)
        article.publie = request.POST.get('publie') == 'on'
        article.save()
        return redirect('public:list_articles')
    
    return render(request, 'public/edit_article.html', {'article': article})

@login_required(login_url='public:login')
def list_messages_contact(request):
    """Liste tous les messages de contact avec gestion des actions"""
    if request.method == 'POST':
        action = request.POST.get('action')
        message_id = request.POST.get('message_id')
        message = get_object_or_404(MessageContact, id=message_id)
        
        if action == 'mark_as_treated':
            message.traite = True
            message.save()
            from django.contrib import messages as django_messages
            django_messages.success(request, f"Message de {message.nom} marqué comme traité.")
        elif action == 'delete':
            nom_sender = message.nom
            message.delete()
            from django.contrib import messages as django_messages
            django_messages.success(request, f"Message de {nom_sender} supprimé.")
    
    messages_list = MessageContact.objects.all().order_by('-date_envoi')
    messages_count = MessageContact.objects.count()
    messages_traites = MessageContact.objects.filter(traite=True).count()
    messages_non_traites = MessageContact.objects.filter(traite=False).count()
    
    context = {
        'messages': messages_list,
        'messages_count': messages_count,
        'messages_traites': messages_traites,
        'messages_non_traites': messages_non_traites,
    }
    return render(request, 'public/list_messages_contact.html', context)

@login_required(login_url='public:login')
def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    
    if request.method == 'POST':
        article.delete()
        return redirect('public:list_articles')
    
    return render(request, 'public/delete_article.html', {'article': article})

# ==================== CRÉATIONS GÉNÉRIQUES (sans parent en URL) ====================
@login_required(login_url='public:login')
def create_filiere_generic(request):
    """Création de filière depuis la liste générale avec sélection de centre"""
    centres = Centre.objects.select_related('ville__province').all()
    
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        centre_id = request.POST.get('centre')
        
        if nom and centre_id:
            centre = get_object_or_404(Centre, id=centre_id)
            Filiere.objects.create(
                nom=nom,
                description=description,
                centre=centre
            )
            return redirect('public:list_filieres')
    
    return render(request, 'public/create_filiere_generic.html', {'centres': centres})

@login_required(login_url='public:login')
def create_niveau_generic(request):
    """Création de niveau depuis la liste générale avec sélection de filière"""
    filieres = Filiere.objects.select_related('centre').all()
    
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        filiere_id = request.POST.get('filiere')
        
        if nom and filiere_id:
            filiere = get_object_or_404(Filiere, id=filiere_id)
            Niveau.objects.create(
                nom=nom,
                description=description,
                filiere=filiere
            )
            return redirect('public:list_niveaux')
    
    return render(request, 'public/create_niveau_generic.html', {'filieres': filieres})

@login_required(login_url='public:login')
def create_module_generic(request):
    """Création de module depuis la liste générale avec sélection de niveau"""
    niveaux = Niveau.objects.select_related('filiere__centre').all()
    
    if request.method == 'POST':
        code = request.POST.get('code')
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        niveau_id = request.POST.get('niveau')
        
        if code and nom and niveau_id:
            niveau = get_object_or_404(Niveau, id=niveau_id)
            Module.objects.create(
                code=code,
                nom=nom,
                description=description,
                niveau=niveau
            )
            return redirect('public:list_modules')
    
    return render(request, 'public/create_module_generic.html', {'niveaux': niveaux})

# ==================== GESTION DES ADMINISTRATEURS ====================
@login_required(login_url='public:login')
def list_administrateurs(request):
    # Vérifier que l'utilisateur est admin principal
    try:
        admin_profile = AdminProfile.objects.get(user=request.user)
        if not admin_profile.is_admin_principal():
            return redirect('public:dashboard')
    except AdminProfile.DoesNotExist:
        return redirect('public:dashboard')
    
    administrateurs = AdminProfile.objects.select_related('user', 'centre').all()
    return render(request, 'public/list_administrateurs.html', {'administrateurs': administrateurs})

@login_required(login_url='public:login')
def create_administrateur(request):
    # Vérifier que l'utilisateur est admin principal
    try:
        admin_profile = AdminProfile.objects.get(user=request.user)
        if not admin_profile.is_admin_principal():
            return redirect('public:dashboard')
    except AdminProfile.DoesNotExist:
        return redirect('public:dashboard')
    
    centres = Centre.objects.all()
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        role = request.POST.get('role')
        centre_id = request.POST.get('centre')
        
        if username and password and role:
            if role == 'SOUS-ADMIN' and not centre_id:
                error = 'Le centre est obligatoire pour un sous-administrateur.'
                return render(request, 'public/create_administrateur.html', {'centres': centres, 'error': error})

            from django.contrib.auth.models import User
            try:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.is_staff = True
                user.save()
                
                centre = None
                if centre_id and role == 'SOUS-ADMIN':
                    centre = get_object_or_404(Centre, id=centre_id)
                
                AdminProfile.objects.create(
                    user=user,
                    role=role,
                    centre=centre
                )
                return redirect('public:list_administrateurs')
            except Exception as e:
                error = f"Erreur: {str(e)}"
                return render(request, 'public/create_administrateur.html', {'centres': centres, 'error': error})
    
    return render(request, 'public/create_administrateur.html', {'centres': centres})

@login_required(login_url='public:login')
def edit_administrateur(request, admin_id):
    # Vérifier que l'utilisateur est admin principal
    try:
        admin_profile = AdminProfile.objects.get(user=request.user)
        if not admin_profile.is_admin_principal():
            return redirect('public:dashboard')
    except AdminProfile.DoesNotExist:
        return redirect('public:dashboard')

    admin = get_object_or_404(AdminProfile, id=admin_id)
    centres = Centre.objects.all()
    error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        role = request.POST.get('role')
        centre_id = request.POST.get('centre')
        actif = request.POST.get('actif') == 'on'

        if username and role:
            user = admin.user
            user.username = username
            user.email = email or ''
            if password:
                user.set_password(password)
            user.is_staff = True
            try:
                user.save()
            except Exception as e:
                error = f"Erreur : {str(e)}"
                return render(request, 'public/edit_administrateur.html', {
                    'admin': admin,
                    'centres': centres,
                    'error': error
                })

            centre = None
            if role == 'SOUS-ADMIN':
                if centre_id:
                    centre = get_object_or_404(Centre, id=centre_id)
                else:
                    error = "Le centre est obligatoire pour un sous-administrateur."
            
            if not error:
                if role == 'ADMIN-PRINCIPAL':
                    centre = None

                admin.role = role
                admin.centre = centre
                admin.actif = actif
                admin.save()
                return redirect('public:list_administrateurs')

    return render(request, 'public/edit_administrateur.html', {
        'admin': admin,
        'centres': centres,
        'error': error
    })

@login_required(login_url='public:login')
def delete_administrateur(request, admin_id):
    # Vérifier que l'utilisateur est admin principal
    try:
        admin_profile = AdminProfile.objects.get(user=request.user)
        if not admin_profile.is_admin_principal():
            return redirect('public:dashboard')
    except AdminProfile.DoesNotExist:
        return redirect('public:dashboard')
    
    admin = get_object_or_404(AdminProfile, id=admin_id)
    
    if request.method == 'POST':
        user = admin.user
        admin.delete()
        user.delete()
        return redirect('public:list_administrateurs')
    
    return render(request, 'public/delete_administrateur.html', {'admin': admin})

# ==================== GESTION DES PARAMÈTRES ====================

@login_required(login_url='public:login')
def mon_profil(request):
    try:
        admin_profile = AdminProfile.objects.get(user=request.user)
    except AdminProfile.DoesNotExist:
        admin_profile = None
    
    if request.method == 'POST':
        # Mettre à jour le profil utilisateur
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.last_name = request.POST.get('last_name', request.user.last_name)
        request.user.email = request.POST.get('email', request.user.email)
        request.user.save()
        
        # Message de succès
        message = "Profil mis à jour avec succès!"
        return render(request, 'public/mon_profil.html', {
            'admin_profile': admin_profile,
            'message': message
        })
    
    return render(request, 'public/mon_profil.html', {
        'admin_profile': admin_profile
    })
from django.shortcuts import get_object_or_404, render
from .models import Article

def detail_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'public/detail_article.html', {
        'article': article
    })