import mongoengine 

def global_init():
    # Alias can connect to multiple databases at once
    # Name of the database
    alias_core = "core"
    db = "idk"
    mongoengine.register_connection(alias = alias_core, name = db)