# Mon Site Django

Un site web moderne avec interface publique et administration Django.

## Fonctionnalités

### Interface Publique
- Page d'accueil avec héros et derniers articles
- Page "À propos" avec présentation de l'entreprise
- Formulaire de contact fonctionnel
- Design responsive avec Bootstrap 5
- Animations CSS et effets visuels

### Interface Admin
- Administration des articles (création, modification, publication)
- Gestion des messages de contact
- Interface personnalisée avec actions en lot
- Filtres et recherche avancée

## Installation

1. **Créer l'environnement virtuel**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Appliquer les migrations**
   ```bash
   python manage.py migrate
   ```

4. **Créer un superutilisateur**
   ```bash
   python manage.py createsuperuser
   ```

5. **Démarrer le serveur**
   ```bash
   python manage.py runserver
   ```

## Accès

- **Site public**: http://127.0.0.1:8000/
- **Administration**: http://127.0.0.1:8000/admin/

## Structure du Projet

```
monsite/
├── monsite/           # Configuration du projet
├── public/            # Application principale
│   ├── models.py      # Modèles de données
│   ├── views.py       # Vues de l'interface publique
│   ├── forms.py       # Formulaires
│   ├── admin.py       # Configuration de l'admin
│   ├── templates/     # Templates HTML
│   └── static/        # Fichiers statiques (CSS, JS)
├── db.sqlite3         # Base de données
└── requirements.txt   # Dépendances Python
```

## Modèles de Données

### Article
- titre: Titre de l'article
- contenu: Contenu de l'article
- date_creation: Date de création
- date_modification: Date de dernière modification
- publie: Statut de publication

### MessageContact
- nom: Nom de l'expéditeur
- email: Email de l'expéditeur
- sujet: Sujet du message
- message: Contenu du message
- date_envoi: Date d'envoi
- traite: Statut de traitement

## Technologies Utilisées

- **Backend**: Django 6.0.5
- **Frontend**: Bootstrap 5, Bootstrap Icons
- **Base de données**: SQLite (développement)
- **Langage**: Python 3

## Développement

### Ajouter de nouvelles pages

1. Créer une vue dans `public/views.py`
2. Ajouter l'URL dans `public/urls.py`
3. Créer le template dans `public/templates/public/`

### Personnaliser l'admin

Modifier `public/admin.py` pour personnaliser l'interface d'administration.

### Styles CSS

Les styles personnalisés sont dans `public/static/public/css/style.css`.

## Licence

Projet créé à des fins éducatives.
