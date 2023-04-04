"""
URL configuration for entreprise project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from comptable.views import code_journal_view, compte_general_view, compte_tiers_view

urlpatterns = [
    path('code_journal/lister', code_journal_view.read, name='home'),

    # code journal
    path('code_journal/ajouter', code_journal_view.create, name='create_code_journal'),
    path('code_journal/modifier/<int:id_object>', code_journal_view.update, name='update_code_journal'),
    path('code_journal/supprimer/<int:id_object>', code_journal_view.remove, name='remove_code_journal'),
    path('code_journal/lister', code_journal_view.read, name='list_code_journal'),

    # compte général
    path('compte_general/ajouter', compte_general_view.create, name='create_compte_general'),
    path('compte_general/modifier/<int:id_object>', compte_general_view.update, name='update_compte_general'),
    path('compte_general/supprimer/<int:id_object>', compte_general_view.remove, name='remove_compte_general'),
    path('compte_general/lister', compte_general_view.read, name='list_compte_general'),

    # compte tiers
    path('compte_tiers/ajouter', compte_tiers_view.create, name='create_compte_tiers'),
    path('compte_tiers/modifier/<int:id_object>', compte_tiers_view.update, name='update_compte_tiers'),
    path('compte_tiers/supprimer/<int:id_object>', compte_tiers_view.remove, name='remove_compte_tiers'),
    path('compte_tiers/lister', compte_tiers_view.read, name='list_compte_tiers'),
]
