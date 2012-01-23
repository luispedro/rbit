from rbit import config
from sqlalchemy import create_engine, and_         
from sqlalchemy.orm import sessionmaker            

def test_config():
    engine = create_engine('sqlite://')
    metadata = config.Base.metadata
    metadata.bind = engine
    metadata.create_all()
    sessionmaker_ = sessionmaker(engine)
    cfg = config.Config('config', sessionmaker_)
    for val in (1,2,'string',[1,2,3]):
        cfg.set('test', 'x', val)
        assert cfg.get('test', 'x') == val

