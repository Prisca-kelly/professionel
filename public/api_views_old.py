from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import connection
import json

@require_http_methods(["GET"])
def api_provinces(request):
    """API endpoint pour récupérer la liste des provinces du Gabon depuis la base de données"""
    try:
        with connection.cursor() as cursor:
            # Récupérer toutes les provinces
            cursor.execute("SELECT id, nom FROM provinces ORDER BY nom")
            provinces_data = cursor.fetchall()
            
            provinces = []
            for province_row in provinces_data:
                province_id, province_name = province_row
                
                # Récupérer les villes de cette province
                cursor.execute(
                    "SELECT id, nom FROM villes WHERE province_id = %s ORDER BY nom",
                    [province_id]
                )
                cities_data = cursor.fetchall()
                cities = [{"id": city_id, "name": city_name} for city_id, city_name in cities_data]
                
                # Récupérer les centres de formation dans les villes de cette province
                centers = []
                for city_id, _ in cities_data:
                    cursor.execute(
                        """
                        SELECT c.id, c.nom, c.adresse, c.telephone, c.email, v.nom as ville_name
                        FROM centres c
                        JOIN villes v ON c.ville_id = v.id
                        WHERE v.province_id = %s
                        ORDER BY c.nom
                        """,
                        [province_id]
                    )
                    centers_data = cursor.fetchall()
                    for center_id, center_name, center_adresse, center_telephone, center_email, ville_name in centers_data:
                        centers.append({
                            "id": center_id,
                            "name": center_name,
                            "adresse": center_adresse,
                            "telephone": center_telephone,
                            "email": center_email,
                            "ville": ville_name,
                            "type": "Centre de formation"
                        })
                
                # Coordonnées par défaut pour chaque province (à améliorer avec une table coords si nécessaire)
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
                    "id": province_id,
                    "name": province_name,
                    "code": province_name[:3].upper(),
                    "capital": capitals_map.get(province_name, 'Non spécifiée'),
                    "coords": coords_map.get(province_name, [-1.5, 11.5]),
                    "cities": cities,
                    "centers": centers
                })
            
            return JsonResponse({"success": True, "data": provinces})
            
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
        {
            "id": 3,
            "name": "Moyen-Ogooué",
            "code": "MO",
            "capital": "Lambaréné",
            "cities": [
                {"id": 7, "name": "Lambaréné", "province_id": 3},
                {"id": 8, "name": "Fougamou", "province_id": 3},
                {"id": 9, "name": "Ndjolé", "province_id": 3}
            ],
            "centers": [
                {"id": 5, "name": "CFP Lambaréné", "type": "Centre de formation", "province_id": 3}
            ]
        },
        {
            "id": 4,
            "name": "Ngounié",
            "code": "NG",
            "capital": "Mouila",
            "cities": [
                {"id": 10, "name": "Mouila", "province_id": 4},
                {"id": 11, "name": "Fougamou", "province_id": 4},
                {"id": 12, "name": "Mbigou", "province_id": 4}
            ],
            "centers": [
                {"id": 6, "name": "CFP Mouila", "type": "Centre de formation", "province_id": 4}
            ]
        },
        {
            "id": 5,
            "name": "Nyanga",
            "code": "NY",
            "capital": "Tchibanga",
            "cities": [
                {"id": 13, "name": "Tchibanga", "province_id": 5},
                {"id": 14, "name": "Moulengui-Binza", "province_id": 5},
                {"id": 15, "name": "Moabi", "province_id": 5}
            ],
            "centers": [
                {"id": 7, "name": "CFP Tchibanga", "type": "Centre de formation", "province_id": 5}
            ]
        },
        {
            "id": 6,
            "name": "Ogooué-Ivindo",
            "code": "OI",
            "capital": "Makokou",
            "cities": [
                {"id": 16, "name": "Makokou", "province_id": 6},
                {"id": 17, "name": "Mékambo", "province_id": 6},
                {"id": 18, "name": "Ovan", "province_id": 6}
            ],
            "centers": [
                {"id": 8, "name": "CFP Makokou", "type": "Centre de formation", "province_id": 6}
            ]
        },
        {
            "id": 7,
            "name": "Ogooué-Lolo",
            "code": "OL",
            "capital": "Koulamoutou",
            "cities": [
                {"id": 19, "name": "Koulamoutou", "province_id": 7},
                {"id": 20, "name": "Lastoursville", "province_id": 7},
                {"id": 21, "name": "Mouila", "province_id": 7}
            ],
            "centers": [
                {"id": 9, "name": "CFP Koulamoutou", "type": "Centre de formation", "province_id": 7}
            ]
        },
        {
            "id": 8,
            "name": "Ogooué-Maritime",
            "code": "OM",
            "capital": "Port-Gentil",
            "cities": [
                {"id": 22, "name": "Port-Gentil", "province_id": 8},
                {"id": 23, "name": "Omboué", "province_id": 8},
                {"id": 24, "name": "Gamba", "province_id": 8}
            ],
            "centers": [
                {"id": 10, "name": "CFP Port-Gentil", "type": "Centre de formation", "province_id": 8},
                {"id": 11, "name": "Lycée Technique Port-Gentil", "type": "Lycée technique", "province_id": 8}
            ]
        },
        {
            "id": 9,
            "name": "Woleu-Ntem",
            "code": "WN",
            "capital": "Oyem",
            "cities": [
                {"id": 25, "name": "Oyem", "province_id": 9},
                {"id": 26, "name": "Mitzic", "province_id": 9},
                {"id": 27, "name": "Bitam", "province_id": 9}
            ],
            "centers": [
                {"id": 12, "name": "CFP Oyem", "type": "Centre de formation", "province_id": 9},
                {"id": 13, "name": "Lycée Technique Oyem", "type": "Lycée technique", "province_id": 9}
            ]
        }
    ]
    
    return JsonResponse({
        "success": True,
        "data": provinces
    })

@require_http_methods(["GET"])
def api_villes(request, province_id=None):
    """API endpoint pour récupérer la liste des villes par province"""
    if province_id:
        try:
            province_id = int(province_id)
            # Données des villes par province
            villes_par_province = {
                1: [
                    {"id": 1, "name": "Libreville", "province_id": 1},
                    {"id": 2, "name": "Owendo", "province_id": 1},
                    {"id": 3, "name": "Ntoum", "province_id": 1}
                ],
                2: [
                    {"id": 4, "name": "Franceville", "province_id": 2},
                    {"id": 5, "name": "Moanda", "province_id": 2},
                    {"id": 6, "name": "Mounana", "province_id": 2}
                ],
                3: [
                    {"id": 7, "name": "Lambaréné", "province_id": 3},
                    {"id": 8, "name": "Fougamou", "province_id": 3},
                    {"id": 9, "name": "Ndjolé", "province_id": 3}
                ],
                4: [
                    {"id": 10, "name": "Mouila", "province_id": 4},
                    {"id": 11, "name": "Fougamou", "province_id": 4},
                    {"id": 12, "name": "Mbigou", "province_id": 4}
                ],
                5: [
                    {"id": 13, "name": "Tchibanga", "province_id": 5},
                    {"id": 14, "name": "Moulengui-Binza", "province_id": 5},
                    {"id": 15, "name": "Moabi", "province_id": 5}
                ],
                6: [
                    {"id": 16, "name": "Makokou", "province_id": 6},
                    {"id": 17, "name": "Mékambo", "province_id": 6},
                    {"id": 18, "name": "Ovan", "province_id": 6}
                ],
                7: [
                    {"id": 19, "name": "Koulamoutou", "province_id": 7},
                    {"id": 20, "name": "Lastoursville", "province_id": 7},
                    {"id": 21, "name": "Mouila", "province_id": 7}
                ],
                8: [
                    {"id": 22, "name": "Port-Gentil", "province_id": 8},
                    {"id": 23, "name": "Omboué", "province_id": 8},
                    {"id": 24, "name": "Gamba", "province_id": 8}
                ],
                9: [
                    {"id": 25, "name": "Oyem", "province_id": 9},
                    {"id": 26, "name": "Mitzic", "province_id": 9},
                    {"id": 27, "name": "Bitam", "province_id": 9}
                ]
            }
            
            villes = villes_par_province.get(province_id, [])
            
            return JsonResponse({
                "success": True,
                "data": villes
            })
        except ValueError:
            return JsonResponse({
                "success": False,
                "error": "ID de province invalide"
            }, status=400)
    else:
        # Toutes les villes si aucune province spécifiée
        toutes_villes = []
        for province_id in range(1, 10):
            villes_par_province = {
                1: ["Libreville", "Owendo", "Ntoum"],
                2: ["Franceville", "Moanda", "Mounana"],
                3: ["Lambaréné", "Fougamou", "Ndjolé"],
                4: ["Mouila", "Fougamou", "Mbigou"],
                5: ["Tchibanga", "Moulengui-Binza", "Moabi"],
                6: ["Makokou", "Mékambo", "Ovan"],
                7: ["Koulamoutou", "Lastoursville", "Mouila"],
                8: ["Port-Gentil", "Omboué", "Gamba"],
                9: ["Oyem", "Mitzic", "Bitam"]
            }
            
            for i, ville_name in enumerate(villes_par_province.get(province_id, []), 1):
                toutes_villes.append({
                    "id": (province_id - 1) * 3 + i,
                    "name": ville_name,
                    "province_id": province_id
                })
        
        return JsonResponse({
            "success": True,
            "data": toutes_villes
        })

@require_http_methods(["GET"])
def api_centres(request, province_id=None):
    """API endpoint pour récupérer la liste des centres de formation par province"""
    if province_id:
        try:
            province_id = int(province_id)
            # Données des centres par province
            centres_par_province = {
                1: [
                    {"id": 1, "name": "CFP Libreville", "type": "Centre de formation", "province_id": 1, "specialty": "Numérique"},
                    {"id": 2, "name": "Lycée d'Enseignement Technique", "type": "Lycée technique", "province_id": 1, "specialty": "Génie civil"}
                ],
                2: [
                    {"id": 3, "name": "CFP Franceville", "type": "Centre de formation", "province_id": 2, "specialty": "Mines"},
                    {"id": 4, "name": "Lycée Technique de Franceville", "type": "Lycée technique", "province_id": 2, "specialty": "Industriel"}
                ],
                3: [
                    {"id": 5, "name": "CFP Lambaréné", "type": "Centre de formation", "province_id": 3, "specialty": "Agriculture"}
                ],
                4: [
                    {"id": 6, "name": "CFP Mouila", "type": "Centre de formation", "province_id": 4, "specialty": "Administration"}
                ],
                5: [
                    {"id": 7, "name": "CFP Tchibanga", "type": "Centre de formation", "province_id": 5, "specialty": "Tourisme"}
                ],
                6: [
                    {"id": 8, "name": "CFP Makokou", "type": "Centre de formation", "province_id": 6, "specialty": "Forêt"}
                ],
                7: [
                    {"id": 9, "name": "CFP Koulamoutou", "type": "Centre de formation", "province_id": 7, "specialty": "Élevage"}
                ],
                8: [
                    {"id": 10, "name": "CFP Port-Gentil", "type": "Centre de formation", "province_id": 8, "specialty": "Pétrochimie"},
                    {"id": 11, "name": "Lycée Technique Port-Gentil", "type": "Lycée technique", "province_id": 8, "specialty": "Maritime"}
                ],
                9: [
                    {"id": 12, "name": "CFP Oyem", "type": "Centre de formation", "province_id": 9, "specialty": "Bois"},
                    {"id": 13, "name": "Lycée Technique Oyem", "type": "Lycée technique", "province_id": 9, "specialty": "Agroalimentaire"}
                ]
            }
            
            centres = centres_par_province.get(province_id, [])
            
            return JsonResponse({
                "success": True,
                "data": centres
            })
        except ValueError:
            return JsonResponse({
                "success": False,
                "error": "ID de province invalide"
            }, status=400)
    else:
        # Tous les centres si aucune province spécifiée
        tous_centres = []
        for province_id in range(1, 10):
            centres_par_province = {
                1: ["CFP Libreville", "Lycée d'Enseignement Technique"],
                2: ["CFP Franceville", "Lycée Technique de Franceville"],
                3: ["CFP Lambaréné"],
                4: ["CFP Mouila"],
                5: ["CFP Tchibanga"],
                6: ["CFP Makokou"],
                7: ["CFP Koulamoutou"],
                8: ["CFP Port-Gentil", "Lycée Technique Port-Gentil"],
                9: ["CFP Oyem", "Lycée Technique Oyem"]
            }
            
            for centre_name in centres_par_province.get(province_id, []):
                tous_centres.append({
                    "name": centre_name,
                    "type": "Centre de formation",
                    "province_id": province_id
                })
        
        return JsonResponse({
            "success": True,
            "data": tous_centres
        })
