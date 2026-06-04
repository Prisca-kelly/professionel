# Installation et Configuration MySQL pour le Projet Django

## Étapes d'Installation MySQL sur Windows

### 1. Télécharger et Installer MySQL

1. **Télécharger MySQL Server** :
   - Allez sur : https://dev.mysql.com/downloads/mysql/
   - Téléchargez "MySQL Community Server" pour Windows
   - Choisissez la version 8.0.x (recommandée)

2. **Installation** :
   - Lancez l'installateur
   - Choisissez "Developer Default" ou "Server only"
   - Configurez le mot de passe root (notez-le bien !)
   - Cochez "Configure MySQL Server as a Windows Service"
   - Terminez l'installation

### 2. Ajouter MySQL au PATH Windows

1. **Trouver le chemin d'installation** :
   - Généralement : `C:\Program Files\MySQL\MySQL Server 8.0\bin`

2. **Ajouter au PATH** :
   - Panneau de configuration → Système → Avancé → Variables d'environnement
   - Modifier la variable "Path"
   - Ajouter le chemin du dossier bin de MySQL

### 3. Configurer la Base de Données

1. **Ouvrir MySQL** :
   ```bash
   mysql -u root -p
   ```

2. **Créer la base de données** :
   ```sql
   CREATE DATABASE ministere_gabon CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

3. **Vérifier la création** :
   ```sql
   SHOW DATABASES;
   ```

### 4. Mettre à jour la Configuration Django

Le fichier `settings.py` est déjà configuré avec :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ministere_gabon',
        'USER': 'root',
        'PASSWORD': '',  # Mettez votre mot de passe ici
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

**IMPORTANT** : Mettez votre mot de passe MySQL dans la ligne `'PASSWORD': ''`

### 5. Tester la Connexion

1. **Migrations** :
   ```bash
   python manage.py makemigrations
   ```

2. **Appliquer les migrations** :
   ```bash
   python manage.py migrate
   ```

3. **Créer le superutilisateur** :
   ```bash
   python manage.py createsuperuser
   ```

4. **Démarrer le serveur** :
   ```bash
   python manage.py runserver
   ```

### 6. Alternative : XAMPP/WAMP

Si vous préférez une solution plus simple :

1. **Installer XAMPP** : https://www.apachefriends.org/fr/download.html
2. **Démarrer MySQL** depuis le panneau de contrôle XAMPP
3. **Utiliser phpMyAdmin** : http://localhost/phpmyadmin
4. **Créer la base de données** `ministere_gabon`
5. **Utiliser les identifiants** :
   - User: root
   - Password: (vide par défaut)

### 7. Vérification

Une fois MySQL installé et configuré, testez avec :

```bash
python manage.py check
```

Si tout est correct, vous devriez voir : "System check identified no issues"

## Dépendances Installées

✅ `mysqlclient==2.2.8` - Connecteur Python pour MySQL
✅ Configuration Django mise à jour
✅ `requirements.txt` mis à jour

## Prochaines Étapes

1. Installez MySQL Server sur votre machine
2. Créez la base de données `ministere_gabon`
3. Mettez votre mot de passe dans `settings.py`
4. Lancez les migrations
5. Testez l'application

---

**Note** : Si vous rencontrez des problèmes, vous pouvez temporairement revenir à SQLite en changeant la configuration dans `settings.py`.
