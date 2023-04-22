import pytest

from sqlalchemy.orm import Session
from ...models import UserSummary
from ...services import UserService

root = UserSummary(pid=999999999, onyen='root', first_name="Super", last_name="User",
             email="root@cs.unc.edu", pronouns="they / them")

sol_student = UserSummary(pid=100000000, onyen='sol', first_name="Sol",
               last_name="Student", email="sol@unc.edu", pronouns="they / them")

root_updated = UserSummary(id=1, pid=100000002, onyen='merritt', first_name="Merritt",
               last_name="Manager", email="merritt@unc.edu", pronouns="they / them")

@pytest.fixture()
def user_service(test_session: Session):
    return UserService(test_session)

def test_no_users(user_service: UserService):
    """Tests that the test session initially contains no users"""
    assert len(user_service.all()) is 0

def test_create_user(user_service: UserService):
    """Tests that user can be added to table using save() method"""
    user_service.save(root)
    assert len(user_service.all()) is 1

def test_get_all_users(user_service: UserService):
    """Tests that all users can be retrieved using all() method"""
    user_service.save(root)
    assert len(user_service.all()) is 1
    user_service.save(sol_student)
    assert len(user_service.all()) is 2
    assert user_service.all()[1].id is 2

def test_search_users(user_service: UserService):
    """Tests that a user can be searched for by their name using search()"""
    user_service.save(sol_student)
    found_users = user_service.search(root, "Sol")
    assert found_users[0].first_name == "Sol"

def test_delete(user_service: UserService):
    """Tests that a user is removed from the table when calling delete()"""
    user_service.save(root)
    assert len(user_service.all()) is 1
    user_service.delete(999999999)
    assert len(user_service.all()) is 0

def test_update(user_service: UserService):
    """Tests that an existing user is modified when calling save() with an updated user"""
    user1 = user_service.save(root)
    assert user1.first_name == "Super"
    new_user = user_service.save(root_updated)
    assert root_updated.first_name == new_user.first_name