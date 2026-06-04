#!/usr/bin/env python
"""
Script to create admin users with roles
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monsite.settings')
django.setup()

from django.contrib.auth.models import User
from public.models import AdminProfile, Centre, Ville, Province

def create_admins():
    # Get or create province/ville/centre
    gabon, _ = Province.objects.get_or_create(
        nom='Gabon'
    )
    
    libreville, _ = Ville.objects.get_or_create(
        nom='Libreville',
        province=gabon
    )
    
    centre, _ = Centre.objects.get_or_create(
        nom='Centre de Formation Libreville',
        defaults={
            'ville': libreville,
            'telephone': '+241-1-23-45-67',
            'email': 'centre@gabonpro.com',
            'type_centre': 'Centre de formation'
        }
    )
    
    # Create ADMIN-PRINCIPAL
    if not User.objects.filter(username='kellyprisca733@gmail.com').exists():
        admin1 = User.objects.create_user(
            username='kellyprisca733@gmail.com',
            email='kellyprisca733@gmail.com',
            password='kelly122',
            is_staff=True,
            is_superuser=True,
            first_name='Kelly',
            last_name='Prisca'
        )
        AdminProfile.objects.create(
            user=admin1,
            role='ADMIN-PRINCIPAL',
            actif=True
        )
        print("✓ ADMIN-PRINCIPAL créé: kellyprisca733@gmail.com")
    else:
        print("✓ ADMIN-PRINCIPAL existe déjà: kellyprisca733@gmail.com")
    
    # Create SOUS-ADMIN
    if not User.objects.filter(username='sousadmin@gabonpro.com').exists():
        admin2 = User.objects.create_user(
            username='sousadmin@gabonpro.com',
            email='sousadmin@gabonpro.com',
            password='admin123',
            is_staff=True,
            first_name='Sous',
            last_name='Admin'
        )
        AdminProfile.objects.create(
            user=admin2,
            role='SOUS-ADMIN',
            centre=centre,
            actif=True
        )
        print("✓ SOUS-ADMIN créé: sousadmin@gabonpro.com")
    else:
        print("✓ SOUS-ADMIN existe déjà: sousadmin@gabonpro.com")
    
    print("\n✅ Administrateurs configurés avec succès!")
    print("\nIdentifiants de connexion:")
    print("─" * 50)
    print("ADMIN PRINCIPAL:")
    print("  Email: kellyprisca733@gmail.com")
    print("  Mot de passe: kelly122")
    print("  Accès: Complet au système")
    print("\nSOUS-ADMIN:")
    print("  Email: sousadmin@gabonpro.com")
    print("  Mot de passe: admin123")
    print("  Accès: Centre - Libreville uniquement")
    print("─" * 50)

if __name__ == '__main__':
    create_admins()
