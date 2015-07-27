from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^setup/$', views.setup),
	url(r'^setup/create-teams/$', views.create_teams),
	url(r'^big-board/$', views.big_board),
	url(r'^big-board/selection/(?P<draft_round>[^/]+)/(?P<pick_number>[^/]+)/$', views.make_pick)
]