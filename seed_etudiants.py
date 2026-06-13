from public.models import Etudiant, Niveau, StatutEtudiant
import random
from datetime import date, timedelta

print("🚀 SEED ETUDIANTS START")

niveaux = list(Niveau.objects.all())
statuts = list(StatutEtudiant.objects.all())

if not niveaux:
    print("❌ Aucun niveau trouvé")
if not statuts:
    print("❌ Aucun statut trouvé")

prenoms = ["Jean", "Marie", "Paul", "Claire", "David", "Sophie", "Luc", "Emma", "Andre", "Pierre"]
noms = ["Ndong", "Moussavou", "Obiang", "Ondo", "Mba", "Ngoma", "Biyoghe", "Assoumou", "Nzamba", "Okouyi"]

for i in range(150):
    nom = random.choice(noms)
    prenom = random.choice(prenoms)

    Etudiant.objects.get_or_create(
        matricule=f"MAT{i:05d}",
        defaults={
            "nom": nom,
            "prenom": prenom,
            "sexe": random.choice(["M", "F"]),
            "date_naissance": date(1998, 1, 1) + timedelta(days=random.randint(0, 9000)),
            "telephone": f"07{i:08d}",
            "email": f"{prenom.lower()}.{nom.lower()}{i}@gabon.edu",
            "adresse": "Libreville",
            "niveau": random.choice(niveaux),
            "statut": random.choice(statuts),
        }
    )

print("✔ ETUDIANTS OK :", Etudiant.objects.count())