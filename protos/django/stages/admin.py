from django.contrib import admin
from .models import Stage

@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('semestre','semestre_annee','sujet','entreprise','done','branche','niveau')
    list_display_links = ('sujet',)
    search_fields = ('sujet','entreprise','etudiant','description')
    list_filter = ('done', 'confidentiel','semestre_annee',
        'semestre','branche_abbrev','niveau_abbrev','filiere')
