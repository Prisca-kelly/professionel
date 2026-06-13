from public.models import (
    Module, Niveau,
    Professeur,
    ModuleProfesseur,
    Etudiant, Centre, Filiere, StatutEtudiant,
    SupportCours
)
import random

print("🚀 START SEED...")

# =========================
# 1. MODULES
# =========================
modules_base = [
    ("ALG", "Algorithmique"),
    ("BDD", "Bases de Données"),
    ("WEB", "Développement Web"),
    ("SYS", "Systèmes d’Exploitation"),
    ("RES", "Réseaux"),
]

for niveau in Niveau.objects.all():
    for code, nom in modules_base:
        Module.objects.get_or_create(
            code=f"{code}-{niveau.id}",
            nom=f"{nom} - {niveau.nom}",
            niveau=niveau,
            defaults={"description": f"{nom} pour {niveau.nom}"}
        )

print("✔ Modules OK :", Module.objects.count())


# =========================
# 2. MODULE PROFESSEUR
# =========================
profs = list(Professeur.objects.all())
modules = list(Module.objects.all())

for module in modules:
    if profs:
        prof = random.choice(profs)

        ModuleProfesseur.objects.get_or_create(
            module=module,
            professeur=prof,
            annee_academique="2025-2026"
        )

print("✔ ModuleProfesseur OK :", ModuleProfesseur.objects.count())


# =========================
# 3. ETUDIANTS
# =========================
centres = list(Centre.objects.all())
filieres = list(Filiere.objects.all())
niveaux = list(Niveau.objects.all())
statuts = list(StatutEtudiant.objects.all())

for i in range(120):
    Etudiant.objects.get_or_create(
        nom=f"Etudiant{i}",
        prenom="Gabon",
        email=f"etudiant{i}@mail.com",
        centre=random.choice(centres),
        filiere=random.choice(filieres),
        niveau=random.choice(niveaux),
        statut=random.choice(statuts),
    )

print("✔ Etudiants OK :", Etudiant.objects.count())


# =========================
# 4. SUPPORT COURS
# =========================
for module in Module.objects.all():
    SupportCours.objects.get_or_create(
        titre=f"Cours {module.nom}",
        module=module,
        defaults={
            "fichier": "default.pdf"
        }
    )

print("✔ SupportCours OK :", SupportCours.objects.count())

print("🎉 SEED TERMINÉ AVEC SUCCÈS")