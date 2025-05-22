# logements/permissions.py
from rest_framework.permissions import BasePermission

class IsDemarcheur(BasePermission):
    """
    Autorise seulement les utilisateurs ayant is_demarcheur=True à créer un logement.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_demarcheur
