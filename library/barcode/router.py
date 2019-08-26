class KohaRouter:
    """
        This class handles the routing of the queries for the Koha Database. It is a router 
        to handle interaction with models from the Barcode App. `See more on Routers... <https://docs.djangoproject.com/en/2.1/topics/db/multi-db/#database-routers>`_

    """

    def db_for_read(self, model, **hints):
        """
            It suggests the database that should be used for read operations for objects of type model. 
            If the *app_label* of the model indicates a Koha table *koha_data*, then the name of Koha Database 
            **koha_db** is returned. Otherwise, **default** Database is returned.
            
            :param model: *A model schema of one of the Koha Tables* \n
            :param hints: *Used by certain operations to communicate additional info to the router.*
            :return: *The name of the database to chose for read operation*

            .. note:: - `hints` is not required here.
                      - `See more on hints... <https://docs.djangoproject.com/en/2.1/topics/db/multi-db/#hints>`_

        """ 
        if model._meta.app_label == 'koha_data':
            return 'koha_db'
        return 'default'

    def db_for_write(self, model, **hints):
        """
            It suggests the database that should be used for write operations for objects of type model. 
            If the *app_label* of the model indicates a Koha table *koha_data*, then the name of Koha Database 
            **koha_db** is returned. Otherwise, **default** Database is returned.

            :param model: *A model schema of one of the Koha Tables* \n
            :param hints: *Used by certain operations to communicate additional info to the router.*

            :return: *The name of the database to chose for write operation*

            .. note:: - `hints` is not required here.
                      -  Barcode App doesn't require the write access to the Koha Database and should be avoided.

        """ 
        if model._meta.app_label == 'koha_data':
            return 'koha_db'
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        """
            It suggests the database that should be used for performing cross relations for objects of type model. 
            If both *obj1* and *obj2* have the *app_label* indicating a Koha table *koha_data* or both do not 
            belong to Koha Table, then True is returned. Otherwise False is returned if the relation should be prevented. 

            :param obj1: *First Model Object* \n
            :param obj2: *Second Model Object* \n
            :param hints: *Used by certain operations to communicate additional info to the router.*

            :return: *A boolean value indicating the allowance of the relation.*

        """ 
        "Allow any relation if a both models in library app"
        if obj1._meta.app_label == 'koha_data' and obj2._meta.app_label == 'koha_data':
            return True
        # Allow if neither is library app
        elif 'koha_data' not in [obj1._meta.app_label, obj2._meta.app_label]: 
            return True
        return False
    
    def allow_syncdb(self, db, model):
        """
            This definition allows whether the database *db* should be synced or not. Returns True if the database *db* 
            is a Koha database and there is a need for the Django to manage it. Otherwise, returns False if it is a Koha
            database to prevent any creation and alteration on it by Django.

            :param db: *The database for which the query is requested* \n
            :param model: *A model schema of one of the Koha Tables*

            :return: *A boolean value indicating whether to sync db or not.*

        """ 
        if db == 'koha_db' or model._meta.app_label == "koha_data":
            return False # do not syncdb on koha database
        else: # but all other models/databases are fine
            return True