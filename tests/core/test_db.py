from sqlalchemy.engine import Engine
from backend.app.db.session import engine, SessionLocal, get_session

def test_engine_configuration():
    assert isinstance(engine, Engine)
    assert engine.pool.size() == 20
    assert engine.pool._pre_ping is True

def test_session_maker():
    session = SessionLocal()
    assert session.bind == engine
    session.close()

def test_get_session_dependency():
    gen = get_session()
    session = next(gen)
    assert session.bind == engine
    session.close()
