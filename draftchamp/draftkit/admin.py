from django.contrib import admin
from .models import Owner, Team, Player, DraftPick

class PlayerAdmin(admin.ModelAdmin):
    search_fields = ['first_name','last_name']
    list_filter = ('available', 'position',)

admin.site.register(Owner)
admin.site.register(Team)
admin.site.register(Player, PlayerAdmin)
admin.site.register(DraftPick)