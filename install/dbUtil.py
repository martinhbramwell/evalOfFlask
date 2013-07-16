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

    user = orm_db.Table('authenticateduser', engine['metadata'], autoload=True)
    iu = user.insert()
    iu.execute(
               {'nickname': 'Hasan', 'email': 'martinhbramwell@gmail.com', 'about_me': 'admin & comnptroller'}
             , {'nickname': 'Alicia', 'email': 'alicia.factorepo@gmail.com', 'about_me': 'only anonymous'}
             , {'nickname': 'Warehouseman', 'email': 'mhb.warehouseman@gmail.com', 'about_me': 'comptroller'}
              )

# {'nickname': '', 'email': '', 'about_me': ''}

    urs = orm_db.Table('user_roles', engine['metadata'], autoload=True)
    iur = urs.insert()
    iur.execute(  {'role_id': 'COMPT', 'user_id': 1}
                , {'role_id': 'ADMIN', 'user_id': 3}
                , {'role_id': 'ANON', 'user_id': 2}
                , {'role_id': 'COMPT', 'user_id': 3}
               )

# {'role_id': '', 'user_id': }

    ufo = orm_db.Table('followers', engine['metadata'], autoload=True)
    ifo = ufo.insert()
    ifo.execute(  {'follower_id': 1, 'followed_id': 1}
                , {'follower_id': 2, 'followed_id': 2}
                , {'follower_id': 3, 'followed_id': 3}
               )

# {'follower_id': 0, 'followed_id': 0}

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


