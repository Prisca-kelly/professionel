from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Province, Ville, Centre
import json

@require_http_methods(["GET"])
def api_provinces(request):
    """API endpoint pour récupérer la liste des provinces avec villes et centres"""
    try:
        # Récupérer toutes les provinces depuis la base de données
        provinces_list = Province.objects.all().order_by('nom')
        
        provinces = []
        for province in provinces_list:
            # Récupérer les villes de cette province
            villes = province.villes.all().order_by('nom')
            cities = [{"id": v.id, "name": v.nom} for v in villes]
            
            # Récupérer les centres de formation via les villes
            centres = Centre.objects.filter(ville__province=province).order_by('nom')
            centers = [
                {
                    "id": c.id,
                    "name": c.nom,
                    "adresse": c.adresse,
                    "telephone": c.telephone,
                    "email": c.email,
                    "ville": c.ville.nom,
                    "type": c.type_centre
                }
                for c in centres
            ]
            
            # Coordonnées par défaut pour chaque province
            coords_map = {
                'Estuaire': [0.3924, 9.4447],
                'Haut-Ogooue': [-1.6333, 13.5833],
                'Moyen-Ogooue': [-0.7000, 10.2333],
                'Ngounie': [-1.8667, 11.0500],
                'Nyanga': [-3.3500, 11.0500],
                'Ogooue-Ivindo': [2.8333, 12.8667],
                'Ogooue-Lolo': [-1.1333, 12.9833],
                'Ogooue-Maritime': [-0.7167, 8.7833],
                'Woleu-Ntem': [2.0000, 11.5833]
            }
            
            # Capitales par province
            capitals_map = {
                'Estuaire': 'Libreville',
                'Haut-Ogooue': 'Franceville',
                'Moyen-Ogooue': 'Lambarene',
                'Ngounie': 'Mouila',
                'Nyanga': 'Tchibanga',
                'Ogooue-Ivindo': 'Makokou',
                'Ogooue-Lolo': 'Koulamoutou',
                'Ogooue-Maritime': 'Port-Gentil',
                'Woleu-Ntem': 'Oyem'
            }
            
            provinces.append({
                "id": province.id,
                "name": province.nom,
                "code": province.nom[:3].upper(),
                "capital": capitals_map.get(province.nom, 'Non spécifiée'),
                "coords": coords_map.get(province.nom, [-1.5, 11.5]),
                "cities": cities,
                "centers": centers
            })
        
        return JsonResponse({"success": True, "data": provinces})
        
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)

@require_http_methods(["GET"])
def api_villes(request, province_id=None):
    """API endpoint pour récupérer la liste des villes par province"""
    try:
        if province_id:
            # Récupérer les villes d'une province spécifique
            villes = Ville.objects.filter(province_id=province_id).order_by('nom')
            villes_data = [{"id": v.id, "name": v.nom} for v in villes]
            
            return JsonResponse({
                "success": True,
                "data": villes_data
            })
        else:
            # Récupérer toutes les villes avec leur province
            villes = Ville.objects.select_related('province').order_by('province__nom', 'nom')
            villes_data = [
                {
                    "id": v.id,
                    "name": v.nom,
                    "province": v.province.nom,
                    "province_id": v.province.id
                }
                for v in villes
            ]
            
            return JsonResponse({
                "success": True,
                "data": villes_data
            })
                
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)

@require_http_methods(["GET"])
def api_centres(request, province_id=None):
    """API endpoint pour récupérer la liste des centres de formation par province"""
    try:
        if province_id:
            # Récupérer les centres d'une province spécifique
            centres = Centre.objects.filter(
                ville__province_id=province_id
            ).select_related('ville', 'ville__province').order_by('nom')
            
            centres_data = [
                {
                    "id": c.id,
                    "name": c.nom,
                    "adresse": c.adresse,
                    "telephone": c.telephone,
                    "email": c.email,
                    "ville": c.ville.nom,
                    "type": c.type_centre
                }
                for c in centres
            ]
            
            return JsonResponse({
                "success": True,
                "data": centres_data
            })
        else:
            # Récupérer tous les centres avec leur ville et province
            centres = Centre.objects.select_related(
                'ville',
                'ville__province'
            ).order_by('ville__province__nom', 'ville__nom', 'nom')
            
            centres_data = [
                {
                    "id": c.id,
                    "name": c.nom,
                    "adresse": c.adresse,
                    "telephone": c.telephone,
                    "email": c.email,
                    "ville": c.ville.nom,
                    "province": c.ville.province.nom,
                    "province_id": c.ville.province.id,
                    "type": c.type_centre
                }
                for c in centres
            ]
            
            return JsonResponse({
                "success": True,
                "data": centres_data
            })
                
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
