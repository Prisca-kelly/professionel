#!/usr/bin/env python
"""
Script pour créer des sous-admins, un par centre (version nettoyée)
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monsite.settings')
django.setup()

from django.contrib.auth.models import User
from public.models import AdminProfile, Centre

def create_sous_admins():
    print("\n" + "="*70)
    print("🏢 Nettoyage et création des sous-admins par centre")
    print("="*70 + "\n")
    
    # Supprimer les anciens sous-admins (sauf l'admin principal)
    old_sous_admins = AdminProfile.objects.filter(role='SOUS-ADMIN')
    old_count = old_sous_admins.count()
    
    for admin_profile in old_sous_admins:
        user = admin_profile.user
        admin_profile.delete()
        user.delete()
    
    if old_count > 0:
        print(f"✓ {old_count} ancien(s) sous-admin(s) supprimé(s)\n")
    
    centres = Centre.objects.all().order_by('nom')
    
    if not centres.exists():
        print("❌ Aucun centre trouvé!")
        return
    
    count = 0
    sous_admins_data = []
    
    for idx, centre in enumerate(centres, 1):
        # Créer un username/email avec l'index pour l'unicité
        username = f"admin_centre_{idx:02d}"
        email = f"admin_{idx:02d}@gabonpro.com"
        password = f"centre_{idx:02d}_2025"
        
        # Créer l'utilisateur
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=True,
            first_name=f"Admin",
            last_name=centre.nom
        )
        
        # Créer le profil AdminProfile
        AdminProfile.objects.create(
            user=user,
            role='SOUS-ADMIN',
            centre=centre,
            actif=True
        )
        
        count += 1
        sous_admins_data.append({
            'num': idx,
            'username': username,
            'email': email,
            'password': password,
            'centre': centre.nom,
            'ville': centre.ville.nom
        })
    
    # Afficher les identifiants
    print("📋 IDENTIFIANTS DES SOUS-ADMINS PAR CENTRE:\n")
    print("─" * 70)
    
    for data in sous_admins_data:
        print(f"\n#{data['num']} - {data['centre']} ({data['ville']})")
        print(f"   Username: {data['username']}")
        print(f"   Email:    {data['email']}")
        print(f"   Mot de passe: {data['password']}")
    
    print("\n" + "="*70)
    print(f"✅ {count} sous-admin(s) créé(s) avec succès!")
    print("="*70)
    
    # Afficher les statistiques
    total_sous_admins = AdminProfile.objects.filter(role='SOUS-ADMIN', actif=True).count()
    print(f"\n📊 Total des sous-admins actifs: {total_sous_admins}")
    print(f"📊 Total des centres: {Centre.objects.count()}\n")

if __name__ == '__main__':
    create_sous_admins()
