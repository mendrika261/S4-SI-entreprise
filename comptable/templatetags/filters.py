from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db import models
from django.template.defaultfilters import floatformat
from django.utils.timezone import now

from comptable.models import Analyse

register = template.Library()


@register.simple_tag
def total_compte(produit, code_compte, date):
    return intcomma(round(produit.get_total_compte(code_compte, date), 2))


@register.simple_tag
def compte_centre_pourcentage(produit, code_compte, id_centre, date=now()):
    return intcomma(round(produit.get_compte_centre_pourcentage(code_compte, id_centre, date), 2))


@register.simple_tag
def compte_centre_fixe(produit, code_compte, id_centre, date=now()):
    return intcomma(round(produit.get_compte_centre_fixe(code_compte, id_centre, date), 2))


@register.simple_tag
def compte_centre_variable(produit, code_compte, id_centre, date=now()):
    return intcomma(round(produit.get_compte_centre_variable(code_compte, id_centre, date), 2))


@register.simple_tag
def total(produit, date=now()):
    return intcomma(round(produit.get_total(date), 2))


@register.simple_tag
def total_centre_fixe(produit, id_centre, date=now()):
    return intcomma(round(produit.total_fixe(id_centre, date), 2))


@register.simple_tag
def total_centre_variable(produit, id_centre, date=now()):
    return intcomma(round(produit.total_variable(id_centre, date), 2))


@register.simple_tag
def total_centre(produit, id_centre, date=now()):
    return intcomma(round(produit.total_centre(id_centre, date), 2))


@register.simple_tag
def centre_total(centre, date=now()):
    return intcomma(round(centre.get_total(date), 2))


@register.simple_tag
def centre_charge_produit_pourcentage(centre, id_produit, date=now()):
    return intcomma(round(centre.charge_produit_pourcentage(id_produit, date), 2))


@register.simple_tag
def centre_charge_produit_fixe(centre, id_produit, date=now()):
    return intcomma(round(centre.charge_produit_fixe(id_produit, date), 2))


@register.simple_tag
def centre_charge_produit_variable(centre, id_produit, date=now()):
    return intcomma(round(centre.charge_produit_variable(id_produit, date), 2))


@register.simple_tag
def charge_produit_incorporable(centre, id_produit, date=now()):
    return intcomma(round(centre.charge_produit_incorporable(id_produit, date), 2))


@register.simple_tag
def charge_produit_non_incorporable(centre, id_produit, date=now()):
    return intcomma(round(centre.charge_produit_non_incorporable(id_produit, date), 2))


@register.simple_tag
def total_variable_compte(produit, code_compte, date=now()):
    return intcomma(round(produit.total_variable_compte(code_compte, date), 2))


@register.simple_tag
def total_fixe_compte(produit, code_compte, date=now()):
    return intcomma(round(produit.total_fixe_compte(code_compte, date), 2))


@register.simple_tag
def total_total_fixe(produit, date=now()):
    return intcomma(round(produit.total_total_fixe(date), 2))


@register.simple_tag
def total_total_variable(produit, date=now()):
    return intcomma(round(produit.total_total_variable(date), 2))


@register.simple_tag
def repartition_centre_pourcentage(produit, centre_operationnel, centre_structure):
    return intcomma(round(produit.repartition_centre_pourcentage(centre_operationnel, centre_structure), 2))


@register.simple_tag
def repartition_centre(produit, centre_operationnel, centre_structure):
    return intcomma(round(produit.repartition_centre(centre_operationnel, centre_structure), 2))


@register.simple_tag
def repartition_centre_total(produit, centre_operationnel, centre_structure):
    return intcomma(round(produit.repartition_centre_total(centre_operationnel, centre_structure), 2))


@register.simple_tag
def total_general_direct(produit):
    return intcomma(round(produit.total_general_direct(), 2))


@register.simple_tag
def total_general_repartition(produit, centre_structure):
    return intcomma(round(produit.total_general_repartition(centre_structure), 2))


@register.simple_tag
def total_general(produit, centre_structure):
    return intcomma(round(produit.total_general(centre_structure), 2))


@register.simple_tag
def cout(produit, centre):
    return intcomma(round(produit.total_centre(centre.id)/produit.stock, 2))