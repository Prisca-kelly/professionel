from public.models import Module, SupportCours, Professeur
import random

print("🚀 START SEED SUPPORT COURS...")

modules = list(Module.objects.all())
profs = list(Professeur.objects.all())

if not modules:
    print("❌ Aucun module trouvé")
    exit()

for module in modules:
    prof = random.choice(profs) if profs else None

    SupportCours.objects.get_or_create(
        titre=f"Cours - {module.nom}",
        module=module,
        defaults={
            "description": f"Support de cours pour {module.nom}",
            "fichier": "default.pdf",
            "fichier_url": "/media/default.pdf",
            "type_fichier": "pdf",
            "uploaded_by": prof
        }
    )

print("✔ SUPPORT COURS OK :", SupportCours.objects.count())
print("🎉 SEED SUPPORT COURS TERMINÉ")