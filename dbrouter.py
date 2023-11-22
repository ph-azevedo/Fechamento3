from django.contrib.auth.models import User
from core.models import AuxListas, Listas, DjangoSession, AuthGroup, DjangoContentType, AuthPermission, CoreAuxlistas, CoreEmpresas, CoreListas, Default, DefaultGroups, DefaultUserPermissions, DjangoAdminLog, DjangoMigrations
from django.contrib import sessions, contenttypes

class Router(object):
    route_app_labels = [User, AuxListas, Listas, sessions, contenttypes, DjangoSession, AuthGroup, DjangoContentType, AuthPermission, CoreAuxlistas, CoreEmpresas, CoreListas, Default, DefaultGroups, DefaultUserPermissions, DjangoAdminLog, DjangoMigrations]

    def db_for_read(self, model, **hints):
        if model in self.route_app_labels:
            return 'default'
        else:
            return 'vlbooks'

    def db_for_write(self, model, **hints):
        if model in self.route_app_labels:
            return 'default'
        else:
            return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'Core':
            if model_name in self.route_app_labels:
                return db == 'default'
            else:
                return db == 'default'