from django.contrib import admin
from .models import Owner, Team, Player, NFLTeam, DraftPick

admin.site.register(Owner)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(NFLTeam)
admin.site.register(DraftPick)