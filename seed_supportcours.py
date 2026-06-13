from public.models import Module, SupportCours
import random

print("🚀 START SEED SUPPORT COURS...")

modules = list(Module.objects.all())

if not modules:
    print("❌ Aucun module trouvé")
    exit()

for module in modules:
    SupportCours.objects.get_or_create(
        titre=f"Cours - {module.nom}",
        module=module,
        defaults={
            "description": f"Support de cours pour {module.nom}",
            "fichier": "default.pdf",
            "fichier_url": "/media/default.pdf",
            "type_fichier": "pdf",
            "uploaded_by_id": None  # 🔥 IMPORTANT FIX
        }
    )

print("✔ SUPPORT COURS OK :", SupportCours.objects.count())
print("🎉 SEED TERMINÉ")