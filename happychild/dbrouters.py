class WriteDBProtectionError(Exception):
    pass


class PrimaryReplicaRouter(object):
    def db_for_read(self, model, **hints):
        """
        Reads go to replica.
        """
        return 'replica'

    def db_for_write(self, model, **hints):
        """
        Writes always go to primary
        """
        return 'primary'

    def allow_relation(self, obj1, obj2, **hints):
        return obj1._meta.app_label == obj2._meta.app_label

    def allow_migrate(self, db, app_label, model=None, **hints):
        return model and app_label == model._meta.app_label
