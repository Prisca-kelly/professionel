from public.models import Professeur, Centre

noms = [
    ("Ndong", "Jean"),
    ("Moussavou", "Marie"),
    ("Obiang", "Paul"),
    ("Ondo", "Claire"),
    ("Mba", "André"),
    ("Mouniang", "Sophie"),
    ("Ekouma", "Joseph"),
    ("Ntoutoume", "Bernard"),
]

centres = Centre.objects.all()

index = 0

for centre in centres:
    for i in range(5):
        nom, prenom = noms[index % len(noms)]
        index += 1

        Professeur.objects.get_or_create(
            nom=nom,
            prenom=prenom,
            centre=centre,
            defaults={
                "email": f"{prenom.lower()}.{nom.lower()}@gabon.edu",
                "telephone": f"07{centre.id}{i}000000"
            }
        )

print("Professeurs OK :", Professeur.objects.count())