from fastapi.testclient import TestClient

from application.app import app
from application.database import get_session
from application.database import Base
from application.accounts.models import AccountModel
from tests.database import Session
from tests.database import engine
from tests.database import get_session as get_test_session

client = TestClient(app)


def test_get_account():
    # arrange
    Base.metadata.create_all(engine)
    app.dependency_overrides[get_session] = get_test_session

    url = 'get-account/1'

    with Session() as session:
        session.add(AccountModel(
            email='test',
            username='test',
            password='test',
        ))
        session.commit()

    # act
    response = client.get(url)
    response_json = response.json()

    # assert
    assert response.status_code == 200
    assert response_json['id'] == 1
