from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import orm_db
import os.path
import shutil

def load(engine):
    print 'Loading . . . '
    
    lease = orm_db.Table('lease', engine['metadata'], autoload=True)
    il = lease.insert()
    il.execute(    {'official_id': '3e3e', 'official_name': 'Barkersville N44-734', 'nick_name': 'Barkers', 'contract': 'Blabbity, blabbity, blah'}
                , {'official_id': '8e4t', 'official_name': 'Janus D45-888', 'nick_name': 'Janus', 'contract': 'We hold these remarks to be self-contrad...'})

# {'official_id': '', 'official_name': '', 'nick_name': '', 'contract': ''}

    role = orm_db.Table('role', engine['metadata'], autoload=True)
    ir = role.insert()
    ir.execute(   {'id': 'ANON', 'name': 'Anonymous'}
                , {'id': 'ADMIN', 'name': 'Administrator'}
                , {'id': 'COMPT', 'name': 'Comptroller'})

# {'id': '', 'name': ''}

def drop(app_root, engine):
    print 'SqlAlchemy migrate repository {} is being removed now!'.format(SQLALCHEMY_MIGRATE_REPO)
    
    migrate_repo = os.path.join(app_root, SQLALCHEMY_MIGRATE_REPO)
    shutil.rmtree(migrate_repo, ignore_errors=True)
    
    db = orm_db.create_engine(SQLALCHEMY_DATABASE_URI)
    metadata = orm_db.MetaData(db)

    migrate_table = orm_db.Table('migrate_version', engine['metadata'], autoload=True)
    engine['db'].execute(migrate_table.delete())
    
    print '{} is being evacuated now!'.format(SQLALCHEMY_DATABASE_URI)
    orm_db.drop_all()
    

def create():
    print '{} is being instantiated now!'.format(SQLALCHEMY_DATABASE_URI)
    orm_db.create_all()
    if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
        api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    else:
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))

def start_engine():
    print 'Starting engine . . . '
    
    db = orm_db.create_engine(SQLALCHEMY_DATABASE_URI)
    engine = {'db': db, 'metadata': orm_db.MetaData(db)}

    return engine


