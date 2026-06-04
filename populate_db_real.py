#!/usr/bin/env python
"""
Script pour remplir la base de données avec les VRAIES données du Gabon
Provinces, villes, centres de formation réels
"""
import os
import django
from datetime import datetime, timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monsite.settings')
django.setup()

from django.contrib.auth.models import User
from public.models import (
    Province, Ville, Centre, Filiere, Niveau, Professeur, Module, 
    ModuleProfesseur, SupportCours, StatutEtudiant, Etudiant, Article, MessageContact
)

def clear_data():
    """Supprime les données existantes"""
    print("Suppression des données existantes...")
    Etudiant.objects.all().delete()
    StatutEtudiant.objects.all().delete()
    ModuleProfesseur.objects.all().delete()
    SupportCours.objects.all().delete()
    Module.objects.all().delete()
    Professeur.objects.all().delete()
    Niveau.objects.all().delete()
    Filiere.objects.all().delete()
    Centre.objects.all().delete()
    Ville.objects.all().delete()
    Province.objects.all().delete()
    Article.objects.all().delete()
    MessageContact.objects.all().delete()
    print("✓ Données supprimées\n")

def populate_provinces_villes():
    """Crée les 9 provinces du Gabon et leurs villes principales"""
    print("📍 Création des 9 provinces du Gabon et leurs villes...\n")
    
    provinces_data = {
        'Estuaire': ['Libreville', 'Akanda', 'Owendo', 'Kango'],
        'Haut-Ogooué': ['Franceville', 'Moanda', 'Mounana', 'Okondja'],
        'Moyen-Ogooué': ['Lambaréné', 'Ndjolé', 'Fougamou'],
        'Ngounié': ['Mouila', 'Ndendé', 'Fougamou', 'Mbigou'],
        'Nyanga': ['Tchibanga', 'Mayumba'],
        'Ogooué-Ivindo': ['Makokou', 'Booué', 'Mékambo'],
        'Ogooué-Lolo': ['Koulamoutou', 'Lastoursville'],
        'Ogooué-Maritime': ['Port-Gentil', 'Gamba', 'Omboué'],
        'Woleu-Ntem': ['Oyem', 'Bitam', 'Mitzic', 'Medouneu']
    }
    
    provinces = {}
    for prov_nom, villes in provinces_data.items():
        prov = Province.objects.create(nom=prov_nom)
        provinces[prov_nom] = prov
        print(f"  ✓ {prov_nom}")
        for ville_nom in villes:
            Ville.objects.create(nom=ville_nom, province=prov)
            print(f"    └─ {ville_nom}")
    
    return provinces

def populate_centres(provinces):
    """Crée les centres de formation réels du Gabon par province"""
    print("\n🏢 Création des centres de formation professionnelle...\n")
    
    centres_data = {
        'Estuaire': [
            {'nom': 'Centre des Métiers Jean Violas (SEEG)', 'ville': 'Owendo', 'type': 'Centre des Métiers'},
            {'nom': 'Centre International Multisectoriel de Nkok', 'ville': 'Akanda', 'type': 'Centre Multisectoriel'},
            {'nom': 'Institut Supérieur de Technologie (IST)', 'ville': 'Libreville', 'type': 'Institut Technique'},
            {'nom': 'Centre de Formation Basile Ondimba', 'ville': 'Libreville', 'type': 'Centre de Formation'},
        ],
        'Haut-Ogooué': [
            {'nom': 'Centre de Formation Professionnelle de Mvengué', 'ville': 'Franceville', 'type': 'CFP'},
            {'nom': 'Centre de Formation Minier', 'ville': 'Moanda', 'type': 'CFP Spécialisé'},
        ],
        'Moyen-Ogooué': [
            {'nom': 'CFP de Lambaréné', 'ville': 'Lambaréné', 'type': 'CFP'},
            {'nom': 'Centre de Formation de Ndjolé', 'ville': 'Ndjolé', 'type': 'CFP'},
        ],
        'Ngounié': [
            {'nom': 'CFP de Mouila', 'ville': 'Mouila', 'type': 'CFP'},
        ],
        'Nyanga': [
            {'nom': 'CFP de Tchibanga', 'ville': 'Tchibanga', 'type': 'CFP'},
        ],
        'Ogooué-Ivindo': [
            {'nom': 'CFP de Makokou', 'ville': 'Makokou', 'type': 'CFP'},
            {'nom': 'Centre de Formation de Booué', 'ville': 'Booué', 'type': 'CFP'},
        ],
        'Ogooué-Lolo': [
            {'nom': 'CFP de Koulamoutou', 'ville': 'Koulamoutou', 'type': 'CFP'},
        ],
        'Ogooué-Maritime': [
            {'nom': 'Centre Multisectoriel de Ntchengue', 'ville': 'Port-Gentil', 'type': 'Centre Multisectoriel'},
            {'nom': 'Centre de Formation Pétrolière', 'ville': 'Port-Gentil', 'type': 'CFP Spécialisé'},
        ],
        'Woleu-Ntem': [
            {'nom': 'CFP d\'Oyem', 'ville': 'Oyem', 'type': 'CFP'},
        ],
    }
    
    centres = []
    for province_nom, centres_list in centres_data.items():
        province = provinces[province_nom]
        print(f"  {province_nom}:")
        for centre_info in centres_list:
            ville = Ville.objects.get(nom=centre_info['ville'])
            centre = Centre.objects.create(
                nom=centre_info['nom'],
                ville=ville,
                adresse=f"Centre de formation professionnelle",
                telephone=f"+241 7 {random.randint(100000, 999999)}",
                email=centre_info['nom'].lower().replace(' ', '_') + '@gabonpro.com',
                type_centre=centre_info['type']
            )
            centres.append(centre)
            print(f"    ✓ {centre.nom}")
    
    return centres

def populate_filieres_niveaux(centres):
    """Crée les filières avec les niveaux corrects (CAP, BEP, BAC pro, BTS, Licence pro)"""
    print("\n📚 Création des filières et niveaux de formation...\n")
    
    filieres_data = [
        {
            'nom': 'Informatique et Développement Web',
            'description': 'Développement web, programmation et technologies numériques',
            'centre': centres[0],
            'niveaux': ['CAP', 'BEP', 'BAC Professionnel', 'BTS', 'Licence Professionnelle']
        },
        {
            'nom': 'Électrotechnique',
            'description': 'Électricité bâtiment, industrielle et maintenance',
            'centre': centres[1],
            'niveaux': ['CAP', 'BEP', 'BAC Professionnel', 'BTS']
        },
        {
            'nom': 'Gestion & Comptabilité',
            'description': 'Comptabilité générale, trésorerie et gestion financière',
            'centre': centres[0],
            'niveaux': ['CAP', 'BEP', 'BAC Professionnel', 'BTS', 'Licence Professionnelle']
        },
        {
            'nom': 'Mécanique Automobile',
            'description': 'Réparation, maintenance et diagnostic automobile',
            'centre': centres[2],
            'niveaux': ['CAP', 'BEP', 'BAC Professionnel']
        },
        {
            'nom': 'Tourisme & Hôtellerie',
            'description': 'Gestion hôtelière, service et réception',
            'centre': centres[3],
            'niveaux': ['CAP', 'BEP', 'BAC Professionnel']
        },
        {
            'nom': 'BTP (Bâtiment et Travaux Publics)',
            'description': 'Maçonnerie, charpente, électricité BTP et menuiserie',
            'centre': centres[1],
            'niveaux': ['CAP', 'BEP', 'BAC Professionnel']
        },
        {
            'nom': 'Mines et Géologie',
            'description': 'Exploitation minière et géologie appliquée',
            'centre': centres[4],
            'niveaux': ['BEP', 'BAC Professionnel', 'BTS']
        },
        {
            'nom': 'Pétrole et Gaz',
            'description': 'Maintenance industrielle pétrolière et offshore',
            'centre': centres[7],
            'niveaux': ['BEP', 'BAC Professionnel', 'BTS', 'Licence Professionnelle']
        },
        {
            'nom': 'Agriculture & Élevage',
            'description': 'Agriculture durable, élevage et aquaculture',
            'centre': centres[5],
            'niveaux': ['CAP', 'BEP', 'BAC Professionnel']
        },
        {
            'nom': 'Santé & Aide Soignante',
            'description': 'Formation d\'aide-soignant et assistant médical',
            'centre': centres[6],
            'niveaux': ['CAP', 'BEP', 'BAC Professionnel']
        },
    ]
    
    filieres = []
    for filiere_data in filieres_data:
        niveaux_list = filiere_data.pop('niveaux')
        filiere = Filiere.objects.create(**filiere_data)
        filieres.append(filiere)
        print(f"  ✓ {filiere.nom}")
        
        for i, niveau_nom in enumerate(niveaux_list, 1):
            niveau = Niveau.objects.create(
                nom=f"{niveau_nom}",
                filiere=filiere,
                description=f"Niveau {i}: {niveau_nom} en {filiere.nom}"
            )
            print(f"    └─ {niveau.nom}")
    
    return filieres

def populate_professeurs(centres):
    """Crée les professeurs"""
    print("\n👨‍🏫 Création des professeurs...\n")
    
    prenoms = ['Pierre', 'Marie', 'Jean', 'Sophie', 'Alain', 'Véronique', 'Paul', 'Christine', 
               'David', 'Nathalie', 'Olivier', 'Isabelle', 'Marc', 'Céline', 'Laurent']
    noms = ['Nguema', 'Obame', 'Koumba', 'Mboyo', 'Bivigou', 'Ngoubi', 'Zeng', 'Ondame',
            'Ngoma', 'Dzabala', 'Boundjou', 'Esono', 'Ebang', 'Nkoghe', 'Missombo']
    
    professeurs = []
    for i, centre in enumerate(centres):
        for j in range(2):
            prof = Professeur.objects.create(
                nom=noms[(i*2 + j) % len(noms)],
                prenom=prenoms[(i*2 + j) % len(prenoms)],
                email=f"prof{i}_{j}@gabonpro.com",
                telephone=f"+241 7 {random.randint(100000, 999999)}",
                centre=centre
            )
            professeurs.append(prof)
    
    print(f"  ✓ {len(professeurs)} professeurs créés")
    return professeurs

def populate_modules(professeurs):
    """Crée les modules académiques"""
    print("\n📖 Création des modules académiques...\n")
    
    modules_data = [
        ('DEV001', 'HTML5 et CSS3', 'Fondamentaux du web'),
        ('DEV002', 'JavaScript ES6+', 'Programmation client'),
        ('DEV003', 'PHP et MySQL', 'Programmation serveur'),
        ('DEV004', 'React.js', 'Framework JavaScript moderne'),
        ('ELEC001', 'Circuits Électriques', 'Théorie et pratique des circuits'),
        ('ELEC002', 'Moteurs Électriques', 'Machines tournantes et industrielles'),
        ('COMPT001', 'Comptabilité Générale', 'Principes comptables fondamentaux'),
        ('COMPT002', 'Trésorerie', 'Gestion de caisse et banque'),
        ('AUTO001', 'Moteur et Transmission', 'Système moteur automobile'),
        ('AUTO002', 'Freinage et Suspension', 'Systèmes de sécurité'),
        ('BTP001', 'Maçonnerie', 'Construction et gros œuvre'),
        ('BTP002', 'Électricité BTP', 'Installation électrique du bâtiment'),
        ('MINES001', 'Exploitation Minière', 'Techniques d\'extraction'),
        ('GAZ001', 'Pétrole et Gaz', 'Processus de production pétrolière'),
        ('AGRI001', 'Agriculture Durable', 'Techniques agricoles modernes'),
    ]
    
    niveaux = list(Niveau.objects.all())
    modules = []
    
    for code, nom, desc in modules_data:
        niveau = random.choice(niveaux)
        module = Module.objects.create(
            code=code,
            nom=nom,
            description=desc,
            niveau=niveau
        )
        modules.append(module)
        print(f"  ✓ {code} - {nom}")
    
    return modules

def populate_module_professeur(modules, professeurs):
    """Assigne les professeurs aux modules"""
    print("\n🔗 Assignation professeurs-modules...\n")
    
    for module in modules:
        prof = random.choice(professeurs)
        ModuleProfesseur.objects.create(
            module=module,
            professeur=prof,
            annee_academique='2025-2026'
        )
    
    print(f"  ✓ {len(modules)} assignations créées")

def populate_statuts_etudiants():
    """Crée les statuts d'étudiants"""
    print("\n📋 Création des statuts étudiants...\n")
    
    statuts = ['Actif', 'En Congé', 'Suspendu', 'Diplômé', 'Abandonné']
    statuts_objs = []
    for statut in statuts:
        obj = StatutEtudiant.objects.create(libelle=statut)
        statuts_objs.append(obj)
        print(f"  ✓ {statut}")
    
    return statuts_objs

def populate_etudiants(statuts_etudiants):
    """Crée les étudiants"""
    print("\n👨‍🎓 Création des étudiants...\n")
    
    prenoms = ['Ahmed', 'Mariam', 'Youssef', 'Fatima', 'Jean', 'Pauline', 'Albert', 'Suzanne', 
               'David', 'Claire', 'Olivier', 'Nathalie', 'Marc', 'Isabelle', 'Luc', 'Angélique']
    noms = ['Obiang', 'Ntoutoume', 'Nguema', 'Obame', 'Koumba', 'Mboyo', 'Bivigou', 'Ngoubi',
            'Zeng', 'Ondame', 'Ngoma', 'Dzabala', 'Boundjou', 'Esono', 'Ebang', 'Missombo']
    
    niveaux = list(Niveau.objects.all())
    
    for i in range(100):
        matricule = f"MAT{datetime.now().year}{i+1:04d}"
        etudiant = Etudiant.objects.create(
            matricule=matricule,
            nom=random.choice(noms),
            prenom=random.choice(prenoms),
            sexe=random.choice(['M', 'F']),
            date_naissance=datetime.now().date() - timedelta(days=random.randint(6575, 8000)),
            telephone=f"+241 7 {random.randint(100000, 999999)}",
            email=f"etudiant{i}@gabonpro.com",
            adresse=f"Quartier {random.choice(['Carrefour', 'Akora', 'La Sablière', 'Glass', 'Nkembo'])}",
            niveau=random.choice(niveaux),
            statut=random.choice(statuts_etudiants)
        )
        if (i + 1) % 20 == 0:
            print(f"  ✓ {i + 1} étudiants créés")

def populate_articles():
    """Crée les articles"""
    print("\n📰 Création des articles...\n")
    
    articles_data = [
        {
            'titre': 'Nouvelle inscription aux formations 2025-2026',
            'contenu': 'Les inscriptions pour l\'année académique 2025-2026 sont ouvertes. Inscrivez-vous dès maintenant aux formations de votre choix.',
            'publie': True
        },
        {
            'titre': 'Réussite exceptionnelle de nos étudiants',
            'contenu': 'Félicitations à tous nos étudiants qui ont obtenu leurs diplômes cette année. Le taux de réussite atteint 92%.',
            'publie': True
        },
        {
            'titre': 'Nouveaux partenariats industriels',
            'contenu': 'Nous sommes fiers d\'annoncer nos nouveaux partenariats avec les entreprises du secteur pétrolier et minier.',
            'publie': True
        },
        {
            'titre': 'Inauguration de nouveaux ateliers pédagogiques',
            'contenu': 'Les travaux de rénovation et d\'extension de nos ateliers sont terminés. Découvrez les nouvelles installations.',
            'publie': True
        },
        {
            'titre': 'Programme d\'aide aux étudiants en difficulté',
            'contenu': 'Un programme d\'aide financière et pédagogique a été mis en place pour soutenir les étudiants en difficulté.',
            'publie': True
        },
    ]
    
    for article_data in articles_data:
        Article.objects.create(**article_data)
        print(f"  ✓ {article_data['titre'][:50]}...")
    
    print(f"\n  Total: {len(articles_data)} articles créés")

def populate_supports_cours():
    """Crée les supports de cours"""
    print("\n📚 Création des supports de cours...\n")
    
    admin_user = User.objects.filter(is_superuser=True).first() or User.objects.first()
    
    modules = list(Module.objects.all())
    
    supports_data = [
        {'titre': 'HTML5 - Introduction et Structures', 'description': 'Guide complet HTML5'},
        {'titre': 'CSS3 - Mise en page responsive', 'description': 'Techniques CSS3 avancées'},
        {'titre': 'JavaScript - Variables et Fonctions', 'description': 'Fondamentaux JavaScript'},
        {'titre': 'React Hooks - Tutoriel complet', 'description': 'Programmation React moderne'},
        {'titre': 'PHP - Gestion des bases de données', 'description': 'PHP et MySQL intégrés'},
        {'titre': 'Électricité - Loi d\'Ohm', 'description': 'Circuits électriques fondamentaux'},
        {'titre': 'Moteurs DC et AC', 'description': 'Machines électriques rotatives'},
        {'titre': 'Comptabilité - Plan comptable', 'description': 'Organisation comptable'},
        {'titre': 'Trésorerie - Gestion de caisse', 'description': 'Gestion des flux financiers'},
        {'titre': 'Moteur automobile - Fonctionnement', 'description': 'Anatomie du moteur'},
        {'titre': 'Systèmes de freinage', 'description': 'Freins hydrauliques et pneumatiques'},
        {'titre': 'Maçonnerie - Fondations', 'description': 'Gros œuvre du bâtiment'},
        {'titre': 'Installations électriques BTP', 'description': 'Électricité résidentielle'},
        {'titre': 'Exploitation minière - Géologie', 'description': 'Techniques minières'},
        {'titre': 'Pétrole - Processus de production', 'description': 'Industrie pétrolière'},
        {'titre': 'Agriculture durable - Sols', 'description': 'Agronomie moderne'},
        {'titre': 'Techniques d\'élevage', 'description': 'Élevage professionnel'},
        {'titre': 'Hygiène en santé', 'description': 'Prévention et hygiène'},
        {'titre': 'Urgences médicales', 'description': 'Soins d\'urgence'},
        {'titre': 'Accueil client - Communication', 'description': 'Service client professionnel'},
    ]
    
    for i, support_data in enumerate(supports_data):
        if modules:
            module = modules[i % len(modules)]
            SupportCours.objects.create(
                titre=support_data['titre'],
                description=support_data['description'],
                module=module,
                uploaded_by=admin_user,
                type_fichier='PDF',
                fichier_url=f'https://example.com/supports/{module.code}_{i}.pdf'
            )
            print(f"  ✓ {support_data['titre'][:50]}... (Module: {module.code})")
    
    print(f"\n  Total: {len(supports_data)} supports créés")

def populate_messages_contact():
    """Crée des messages de contact"""
    print("\n💬 Création des messages de contact...\n")
    
    messages_data = [
        {
            'nom': 'Joël Ntoutoume',
            'email': 'joel.ntoutoume@email.com',
            'sujet': 'Demande de renseignements - Informatique Web',
            'message': 'Je voudrais en savoir plus sur le programme de développement web et les conditions d\'admission.'
        },
        {
            'nom': 'Mariette Obame',
            'email': 'mariette.obame@email.com',
            'sujet': 'Inscription formation électrotechnique',
            'message': 'Pourriez-vous me donner les dates d\'inscription et les frais de formation pour l\'électrotechnique?'
        },
        {
            'nom': 'Serge Koumba',
            'email': 'serge.koumba@email.com',
            'sujet': 'Problème d\'accès au portail de formation',
            'message': 'Je ne parviens pas à accéder à mon compte étudiant. Je n\'arrive pas à me connecter.'
        },
        {
            'nom': 'Aline Bivigou',
            'email': 'aline.bivigou@email.com',
            'sujet': 'Demande de certificat de formation complétée',
            'message': 'Pourriez-vous me délivrer un certificat attestant que j\'ai suivi la formation en comptabilité?'
        },
        {
            'nom': 'Théo Nguema',
            'email': 'theo.nguema@email.com',
            'sujet': 'Formation continue - BTS Pétrole et Gaz',
            'message': 'Êtes-vous intéressés par une formation continue en pétrole et gaz pour mon entreprise?'
        },
    ]
    
    for msg_data in messages_data:
        MessageContact.objects.create(**msg_data)
        print(f"  ✓ {msg_data['sujet']}")
    
    print(f"\n  Total: {len(messages_data)} messages créés")

def populate_supports_cours():
    """Crée les supports de cours"""
    print("\n📚 Création des supports de cours...\n")
    
    admin_user = User.objects.filter(is_superuser=True).first() or User.objects.first()
    
    modules = list(Module.objects.all())
    
    supports_data = [
        ('Cours HTML5', 'Guide complet du HTML5 et bonnes pratiques'),
        ('Cours CSS3', 'Tutoriel complet CSS3 et Flexbox'),
        ('JavaScript Avancé', 'Techniques avancées de JavaScript ES6+'),
        ('React Components', 'Création de composants réutilisables'),
        ('PHP MVC', 'Patterns MVC en PHP'),
        ('MySQL Database', 'Design et optimisation de bases de données'),
        ('Circuits Électriques', 'Théorie des circuits pour débutants'),
        ('Moteurs AC/DC', 'Fonctionnement des moteurs électriques'),
        ('Comptabilité', 'Principes fondamentaux de comptabilité'),
        ('Gestion de Trésorerie', 'Techniques de gestion financière'),
        ('Diagnostic Auto', 'Diagnostic moderne des véhicules'),
        ('Freinage Antiblocage', 'Systèmes de freinage modernes'),
        ('Maçonnerie BTP', 'Techniques de construction'),
        ('Électricité Bâtiment', 'Installations électriques conformes'),
        ('Exploitation Minière', 'Techniques d\'extraction et sécurité'),
        ('Sécurité Pétrolière', 'Protocoles de sécurité en offshore'),
        ('Agriculture Biologique', 'Méthodes d\'agriculture durable'),
        ('Premiers Secours', 'Formation de base en premiers secours'),
        ('Comptabilité Avancée', 'Comptabilité analytique'),
        ('Excel Avancé', 'Utilisation avancée d\'Excel'),
    ]
    
    supports_created = 0
    for i, (titre, desc) in enumerate(supports_data):
        module = modules[i % len(modules)]
        
        SupportCours.objects.create(
            titre=titre,
            description=desc,
            module=module,
            uploaded_by=admin_user,
            fichier_url=f'https://exemple-supports.com/supports/{i:03d}.pdf',
            type_fichier='PDF'
        )
        supports_created += 1
    
    print(f"  ✓ {supports_created} supports de cours créés")

def main():
    print("="*70)
    print("🚀 Remplissage de la base de données avec les VRAIES données du GABON")
    print("="*70)
    print()
    
    clear_data()
    
    provinces = populate_provinces_villes()
    centres = populate_centres(provinces)
    filieres = populate_filieres_niveaux(centres)
    professeurs = populate_professeurs(centres)
    modules = populate_modules(professeurs)
    populate_module_professeur(modules, professeurs)
    statuts_etudiants = populate_statuts_etudiants()
    populate_etudiants(statuts_etudiants)
    populate_articles()
    populate_supports_cours()
    populate_messages_contact()
    
    print("\n" + "="*70)
    print("✅ Base de données remplie avec succès!")
    print("="*70)
    print("\n📊 Résumé des données créées:")
    print(f"  • Provinces: {Province.objects.count()}")
    print(f"  • Villes: {Ville.objects.count()}")
    print(f"  • Centres: {Centre.objects.count()}")
    print(f"  • Filières: {Filiere.objects.count()}")
    print(f"  • Niveaux: {Niveau.objects.count()}")
    print(f"  • Professeurs: {Professeur.objects.count()}")
    print(f"  • Modules: {Module.objects.count()}")
    print(f"  • Assignations Prof-Module: {ModuleProfesseur.objects.count()}")
    print(f"  • Supports de cours: {SupportCours.objects.count()}")
    print(f"  • Statuts étudiants: {StatutEtudiant.objects.count()}")
    print(f"  • Étudiants: {Etudiant.objects.count()}")
    print(f"  • Articles: {Article.objects.count()}")
    print(f"  • Messages: {MessageContact.objects.count()}")
    print("="*70)

if __name__ == '__main__':
    main()
