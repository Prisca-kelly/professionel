from django.contrib import admin
from .models import Province, Ville, Centre, Article, MessageContact

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom')
    search_fields = ('nom',)
    ordering = ('nom',)
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('nom',)
        }),
    )

@admin.register(Ville)
class VilleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'province', 'date_creation')
    list_filter = ('province', 'date_creation')
    search_fields = ('nom',)
    ordering = ('nom',)
    readonly_fields = ('date_creation',)
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('nom', 'province')
        }),
    )

@admin.register(Centre)
class CentreAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ville', 'type_centre', 'telephone', 'email', 'date_creation')
    list_filter = ('ville', 'type_centre', 'date_creation')
    search_fields = ('nom', 'adresse', 'telephone', 'email')
    ordering = ('nom',)
    readonly_fields = ('date_creation',)
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('nom', 'type_centre', 'ville')
        }),
        ('Coordonnées', {
            'fields': ('adresse', 'telephone', 'email')
        }),
    )

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date_creation', 'date_modification', 'publie')
    list_filter = ('publie', 'date_creation')
    search_fields = ('titre', 'contenu')
    list_editable = ('publie',)
    ordering = ('-date_creation',)
    date_hierarchy = 'date_creation'
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('titre', 'contenu')
        }),
        ('Publication', {
            'fields': ('publie',),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',),
            'description': 'Dates de création et de modification'
        }),
    )
    
    readonly_fields = ('date_creation', 'date_modification')

@admin.register(MessageContact)
class MessageContactAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'sujet', 'date_envoi', 'traite')
    list_filter = ('traite', 'date_envoi')
    search_fields = ('nom', 'email', 'sujet')
    list_editable = ('traite',)
    ordering = ('-date_envoi',)
    date_hierarchy = 'date_envoi'
    
    fieldsets = (
        ('Expéditeur', {
            'fields': ('nom', 'email')
        }),
        ('Message', {
            'fields': ('sujet', 'message')
        }),
        ('Traitement', {
            'fields': ('traite', 'date_envoi'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('date_envoi',)
    
    actions = ['marquer_comme_traite', 'marquer_comme_non_traite']
    
    def marquer_comme_traite(self, request, queryset):
        queryset.update(traite=True)
        self.message_user(request, f"{queryset.count()} message(s) marqué(s) comme traité(s)")
    marquer_comme_traite.short_description = "Marquer comme traité"
    
    def marquer_comme_non_traite(self, request, queryset):
        queryset.update(traite=False)
        self.message_user(request, f"{queryset.count()} message(s) marqué(s) comme non traité(s)")
    marquer_comme_non_traite.short_description = "Marquer comme non traité"
