from django.urls import path
from . import views
urlpatterns = [path("", views.home, name="home"), path("profils/creer/", views.create_profile, name="create_profile"), path("profils/<int:pk>/", views.select_profile, name="select_profile"), path("tables/<str:operation>/", views.tables, name="tables"), path("demarrer/<str:operation>/<int:table>/", views.start, name="start"), path("exercice/<int:pk>/", views.exercise, name="exercise"), path("historique/", views.history, name="history")]
