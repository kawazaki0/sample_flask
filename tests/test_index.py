import pytest

from sample_flask.app import Entry, db, create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["WTF_CSRF_ENABLED"] = False
    with app.app_context():
        db.init_app(app)
        db.create_all()
        yield app.test_client()


def test_index(client):
    response = client.get("/")
    assert b"Sample Flask" in response.data


def test_form(client):
    response = client.post("/submit", data={
        "key": "test_key",
        "value": "test_value",
    }, follow_redirects=True)
    assert len(Entry.query.all()) == 1
    assert Entry.query.all()[0].key == "test_key"
    assert b"test_key" in response.data
