#!/usr/bin/env python
"""
Seed script PRO - Base de données pédagogique Gabon
Safe re-run + Faker + atomic + scalable
"""

import os
import django
import random
from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "monsite.settings")
django.setup()

from django.contrib.auth.models import User
from public.models import (
    Province, Ville, Centre, Filiere, Niveau, Professeur,
    Module, ModuleProfesseur, StatutEtudiant, Etudiant,
    Article, MessageContact
)

fake = Faker("fr_FR")

# =========================================================
# CONFIG DATA (GABON CLEAN STRUCTURE)
# =========================================================

PROVINCES_DATA = {
    "Estuaire": ["Libreville", "Owendo", "Akanda", "Kango", "Ntoum"],
    "Haut-Ogooué": ["Franceville", "Moanda", "Mounana", "Okondja", "Bongoville"],
    "Moyen-Ogooué": ["Lambaréné", "Ndjolé", "Fougamou"],
    "Ngounié": ["Mouila", "Ndendé", "Tchibanga"],
    "Nyanga": ["Mayumba", "Moabi", "Tchibanga"],
    "Ogooué-Ivindo": ["Makokou", "Booué", "Mekambo"],
    "Ogooué-Lolo": ["Koulamoutou", "Lastoursville", "Pana"],
    "Ogooué-Maritime": ["Port-Gentil", "Omboué", "Gamba"],
    "Woleu-Ntem": ["Oyem", "Bitam", "Mitzic"],
}

FILIERES_DATA = [
    ("Informatique et Développement Web", "Dev web & logiciel"),
    ("Électrotechnique", "Électricité industrielle"),
    ("Gestion & Comptabilité", "Finance et gestion"),
    ("Mécanique Automobile", "Réparation automobile"),
    ("Tourisme & Hôtellerie", "Services touristiques"),
]

MODULES_DATA = [
    ("DEV001", "HTML/CSS"),
    ("DEV002", "JavaScript"),
    ("DEV003", "PHP/MySQL"),
    ("DEV004", "React"),
    ("ELEC001", "Circuits électriques"),
    ("ELEC002", "Machines électriques"),
    ("COMPT001", "Comptabilité générale"),
    ("COMPT002", "Trésorerie"),
    ("AUTO001", "Moteur"),
    ("AUTO002", "Freinage"),
]

STATUTS = ["Actif", "En Congé", "Suspendu", "Diplômé", "Abandonné"]


# =========================================================
# CLEAN FUNCTIONS
# =========================================================

def safe_get_or_create(model, defaults=None, **kwargs):
    obj, created = model.objects.get_or_create(defaults=defaults or {}, **kwargs)
    return obj


# =========================================================
# SEED FUNCTIONS
# =========================================================

def seed_geography():
    print("📍 Géographie...")

    provinces = {}

    for prov_name, villes in PROVINCES_DATA.items():
        province = safe_get_or_create(Province, nom=prov_name)
        provinces[prov_name] = province

        for ville_name in villes:
            safe_get_or_create(Ville, nom=ville_name, province=province)

    return provinces


def seed_centres(provinces):
    print("🏢 Centres...")

    centres = []

    estuaire = provinces["Estuaire"]

    data = [
        ("CFP Libreville", "Libreville"),
        ("Institut Owendo", "Owendo"),
        ("Lycée Port-Gentil", "Port-Gentil"),
        ("École Franceville", "Franceville"),
    ]

    for name, ville in data:
        centre = safe_get_or_create(
            Centre,
            nom=name,
            defaults={
                "ville": Ville.objects.get(nom=ville),
                "adresse": fake.address(),
                "telephone": fake.phone_number(),
                "email": fake.email(),
                "type_centre": fake.random_element([
                    "Centre de Formation",
                    "Institut Technique",
                    "Lycée Technique"
                ])
            }
        )
        centres.append(centre)

    return centres


def seed_filieres(centres):
    print("📚 Filières...")

    filieres = []

    for i, (nom, desc) in enumerate(FILIERES_DATA):
        centre = centres[i % len(centres)]

        filiere = safe_get_or_create(
            Filiere,
            nom=nom,
            defaults={"description": desc, "centre": centre}
        )

        filieres.append(filiere)

        # niveaux
        for lvl in range(1, 4):
            safe_get_or_create(
                Niveau,
                nom=f"Niveau {lvl} - {nom}",
                filiere=filiere,
                defaults={"description": fake.sentence()}
            )

    return filieres


def seed_professeurs(centres):
    print("👨‍🏫 Professeurs...")

    profs = []

    for _ in range(10):
        prof = safe_get_or_create(
            Professeur,
            email=fake.unique.email(),
            defaults={
                "nom": fake.last_name(),
                "prenom": fake.first_name(),
                "telephone": fake.phone_number(),
                "centre": random.choice(centres),
            }
        )
        profs.append(prof)

    return profs


def seed_modules():
    print("📖 Modules...")

    niveaux = list(Niveau.objects.all())

    modules = []

    for i, (code, nom) in enumerate(MODULES_DATA):
        niveau = niveaux[i % len(niveaux)]

        module = safe_get_or_create(
            Module,
            code=code,
            defaults={
                "nom": nom,
                "description": fake.text(),
                "niveau": niveau,
            }
        )

        modules.append(module)

    return modules


def seed_module_professeurs(modules, profs):
    print("🔗 Assignations...")

    for module in modules:
        prof = random.choice(profs)

        safe_get_or_create(
            ModuleProfesseur,
            module=module,
            professeur=prof,
            defaults={"annee_academique": "2025-2026"}
        )


def seed_statuts():
    print("📋 Statuts...")

    return [
        safe_get_or_create(StatutEtudiant, libelle=s)
        for s in STATUTS
    ]


def seed_etudiants(niveaux, statuts):
    print("🎓 Étudiants...")

    for _ in range(50):
        safe_get_or_create(
            Etudiant,
            matricule=f"MAT{timezone.now().year}{random.randint(1000,9999)}",
            defaults={
                "nom": fake.last_name(),
                "prenom": fake.first_name(),
                "sexe": random.choice(["M", "F"]),
                "date_naissance": timezone.now().date() - timedelta(days=random.randint(6000, 9000)),
                "telephone": fake.phone_number(),
                "email": fake.unique.email(),
                "adresse": fake.address(),
                "niveau": random.choice(niveaux),
                "statut": random.choice(statuts),
            }
        )


def seed_articles():
    print("📰 Articles...")

    user = User.objects.filter(is_superuser=True).first() or User.objects.first()

    for _ in range(5):
        safe_get_or_create(
            Article,
            titre=fake.sentence(),
            defaults={
                "contenu": fake.paragraph(nb_sentences=10),
                "publie": True,
            }
        )


def seed_messages():
    print("💬 Messages...")

    for _ in range(5):
        safe_get_or_create(
            MessageContact,
            email=fake.email(),
            defaults={
                "nom": fake.name(),
                "sujet": fake.sentence(),
                "message": fake.text(),
            }
        )


# =========================================================
# MAIN
# =========================================================

@transaction.atomic
def main():
    print("=" * 60)
    print("🚀 SEED DATABASE PRO (SAFE + FAKE DATA + ATOMIC)")
    print("=" * 60)

    provinces = seed_geography()
    centres = seed_centres(provinces)
    seed_filieres(centres)

    profs = seed_professeurs(centres)
    modules = seed_modules()

    seed_module_professeurs(modules, profs)

    statuts = seed_statuts()
    niveaux = list(Niveau.objects.all())

    seed_etudiants(niveaux, statuts)
    seed_articles()
    seed_messages()

    print("\n" + "=" * 60)
    print("✅ DONE")
    print("=" * 60)

    print(f"Provinces: {Province.objects.count()}")
    print(f"Villes: {Ville.objects.count()}")
    print(f"Centres: {Centre.objects.count()}")
    print(f"Filières: {Filiere.objects.count()}")
    print(f"Niveaux: {Niveau.objects.count()}")
    print(f"Professeurs: {Professeur.objects.count()}")
    print(f"Modules: {Module.objects.count()}")
    print(f"Étudiants: {Etudiant.objects.count()}")


if __name__ == "__main__":
    main()