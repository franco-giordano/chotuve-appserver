from app import create_app, db
import pytest
import os
import tempfile

@pytest.yield_fixture(scope='session')
def flask_app():
    app = create_app('testing')

    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()

@pytest.fixture(scope='session')
def testapp(flask_app):
    return flask_app.test_client()

@pytest.fixture(scope='session', autouse=True)
def db_handle(flask_app):
    db_fd, db_fname = tempfile.mkstemp()
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_fname
    
    db.init_app(flask_app)
    db.create_all()
       
    yield db
    
    db.session.remove()
    os.close(db_fd)
    os.unlink(db_fname)