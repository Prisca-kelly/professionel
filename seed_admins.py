from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from public.models import AdminProfile, Centre


class Command(BaseCommand):
    help = "Créer uniquement les 8 Sous-Admins"

    def handle(self, *args, **kwargs):

        centre = Centre.objects.first()

        if not centre:
            self.stdout.write(self.style.ERROR("Aucun centre trouvé"))
            return

        # =========================
        # SOUS-ADMINS UNIQUEMENT
        # =========================

        for i in range(1, 9):
            username = f"sousadmin{i}"

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": f"{username}@site.com",
                    "first_name": f"Sous{i}",
                    "last_name": "Admin",
                    "is_staff": True,
                    "is_superuser": False,
                    "is_active": True,
                }
            )

            if created:
                user.set_password("admin123")
                user.save()

            AdminProfile.objects.get_or_create(
                user=user,
                defaults={
                    "role": "Sous-Admin",
                    "actif": True,
                    "centre": centre
                }
            )

        self.stdout.write(self.style.SUCCESS(
            "✔ 8 Sous-Admins créés avec succès"
        ))