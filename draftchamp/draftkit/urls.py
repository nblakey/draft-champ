from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^setup/$', views.setup),
	url(r'^setup/create-teams/$', views.create_teams),
	url(r'^keepers/$', views.keepers),
	url(r'^keepers/trade/$', views.trade_pick),
	url(r'^keepers/keep/$', views.keep_pick),
	url(r'^big-board/$', views.big_board),
	url(r'^big-board/selection/(?P<overall_pick>[^/]+)/$', views.make_pick),
	url(r'^big-board/recent-picks/$', views.recent_picks),
	url(r'^big-board/rosters/$', views.show_roster)
]